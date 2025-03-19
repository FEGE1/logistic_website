from django.shortcuts import render,redirect
from order import map
from order.views import Form_Create

def IndexView(request):
    if request.method == "POST":
        receiving = request.POST.get("receiving")
        destination = request.POST.get("destination")

        context = {"receiving":receiving,
                   "destination":destination}

        request.session['receiving'] = receiving
        request.session['destination'] = destination
        #return render(request,'order/create_order.html', context=context)
        return redirect('form_create')
    return render(request,'index.html')

def LoginView(request):
    return render(request,'login.html')