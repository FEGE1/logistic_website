from django.urls import path
from order import views
from order.forms import ReceivingLocationForm, DestinationLocationForm, VehicleForm, CargoForm
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage

file_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

app_name = "order"

urlpatterns = [
    path('create-order', views.OrderWizard.as_view(form_list= [ReceivingLocationForm, DestinationLocationForm, CargoForm],
                                                   file_storage= file_storage),
                                                   name= 'create-order'),

    path('order-success', lambda request: render(request, 'order/success.html'),name='order_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
