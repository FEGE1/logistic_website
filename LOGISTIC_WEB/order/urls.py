from django.urls import path
from order import views

urlpatterns = [
    path('',views.Form_view,name='form_view'),
    path('create/',views.Form_Create,name='form_create'),
]
