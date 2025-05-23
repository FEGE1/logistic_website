from django.shortcuts import render, redirect
from order.forms import OrderForm,ReceivingLocationForm,DestinationLocationForm,VehicleForm,CargoForm,BillForm
from order.models import Order, Receiving_location, Destination_location, Vehicle, Cargo, Bill
from order import map
from formtools.wizard.views import SessionWizardView

from django.core.files.storage import FileSystemStorage
from django.conf import settings

def Form_Create(request):
    receiving = request.session.pop('receiving',' ')
    destination = request.session.pop('destination',' ')
    order_code = request.session.pop('order_code',' ')

    context = {
        'receiving': receiving,
        'destination': destination,
        'order_code': order_code
    }
    #order code ile siparişin içinden receiving ve destinationları alıp js e atabilirim (refresh attığımda harita kaybolmasın diye)(indexteyken receiving ve destinationı kaydetmek lazım)
    return render(request,'order/create_order.html', context=context)

class OrderWizard(SessionWizardView):
    
    form_list = [ReceivingLocationForm, DestinationLocationForm, VehicleForm,CargoForm]
    
    template_name = "order/form_wizard.html"

    file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        
        receiving = self.request.session.get('receiving',' ')
        destination = self.request.session.get('destination',' ')

        context['receiving'] = receiving
        context['destination'] = destination

        return context
    
    # Set default value for fields
    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == '0':  # first form (ReceivingLocationForm)
            initial['address'] = self.request.session.get('receiving', '')
        if step == '1':  # second form (DestinationLocationForm)
            initial['address'] = self.request.session.get('destination', '')
        return initial
    
    # Non-validation for go back in forms
    def post(self, *args, **kwargs):  # ← BURAYA
        if 'wizard_goto_step' in self.request.POST:
            self.storage.current_step = self.request.POST['wizard_goto_step']
            return self.render(self.get_form())
        return super().post(*args, **kwargs)
    
    def done(self, form_list, **kwargs):

        calculated_price = self.request.session.pop('calculated_price',' ')

        order = Order.objects.create(
            customer = self.request.user,
            status = 'Aktif',
            price = calculated_price
        )

        form_data = [form.cleaned_data for form in form_list]

        Receiving_location.objects.create(
            order = order,
            **form_data[0] # çift yıldız operatörü gelen data dictionary'sinin içindekileri key = value şeklinde fonksiyonun içine yazar (unpacking)
        )

        Destination_location.objects.create(
            order = order,
            **form_data[1]
        )

        Vehicle.objects.create(
            order = order,
            **form_data[2]
        )

        Cargo.objects.create(
            order = order,
            **form_data[3]
        )

        Bill.objects.create(
        order=order,
        company_name="Default Company",
        address="Default Address",
        name=self.request.user.first_name or "Name",
        surname=self.request.user.last_name or "Surname",
        email=self.request.user.email or "default@example.com",
        satis_vergisi_kimligi="1234567890"
        )

        return redirect('order_success')