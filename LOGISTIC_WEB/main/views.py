from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from order.models import Order
from order.map import calculate_distance

def IndexView(request):
    if request.method == "POST":

        receiving = request.POST.get("receiving")
        destination = request.POST.get("destination")

        calculated_price = calculate_distance(receiving, destination)*20

        user = User.objects.first()

        request.session['receiving'] = receiving
        request.session['destination'] = destination
        request.session['calculated_price'] = calculated_price

        return redirect('order:create-order')
    return render(request,'index.html')