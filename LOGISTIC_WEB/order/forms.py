from django import forms 
from order.models import Order,Receiving_location,Destination_location,Vehicle,Cargo,Bill


class OrderForm(forms.ModelForm):
    class Meta():
        model = Order
        fields = '__all__'

class ReceivingLocationForm(forms.ModelForm):
    class Meta():
        model = Receiving_location
        fields = ('company_name','company_number','address','pickup_date')
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'})
        }

class DestinationLocationForm(forms.ModelForm):
    class Meta():
        model = Destination_location
        fields = ('company_name','company_number','address','delivery_date')
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'})
        }

class VehicleForm(forms.ModelForm):
    class Meta():
        model = Vehicle
        fields = ('type','price_km','max_weight','storage_height','storage_width','storage_length')

class CargoForm(forms.ModelForm):
    class Meta():
        model = Cargo
        fields = ('type','weight','height','width','length','image')

class BillForm(forms.ModelForm):
    class Meta():
        model = Bill
        fields = ('company_name','address','name','surname','email','satis_vergisi_kimligi')