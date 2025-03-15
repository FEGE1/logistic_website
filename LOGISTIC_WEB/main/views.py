from django.shortcuts import render
from order import map

def IndexView(request):
    if request.method == "POST":
        receiving = request.POST.get("receiving")
        destination = request.POST.get("destination")
        print(receiving+" "+destination)

        context = {"receiving":receiving,
                   "destination":destination}

        return render(request,'map_test.html', context=context)
    return render(request,'index.html')

def LoginView(request):
    return render(request,'login.html')

def MapView(request):
    return render(request,'map_test.html')