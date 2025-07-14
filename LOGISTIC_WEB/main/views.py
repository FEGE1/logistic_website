from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from order.models import Order
from order.map import Calculate_Direction
from keys import google_maps_key

def IndexView(request):
    if request.method == "POST":

        receiving = request.POST.get("receiving")
        destination = request.POST.get("destination")

        calculated_distance = Calculate_Direction(receiving, destination)['distance_value']
        price = calculated_distance*20

        user = User.objects.first()

        request.session['receiving'] = receiving
        request.session['destination'] = destination
        request.session['calculated_price'] = price

        return redirect('order:create-order')
    return render(request,'index.html',context={'google_maps_key':google_maps_key})