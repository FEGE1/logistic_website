from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from user.forms import UserMainForm, UserLoginForm

# Create your views here.

def RegisterView(request):
    if request.method == "POST":
        form = UserMainForm(data= request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            login(request,user)
            return redirect('index')
        
        else:
            print(UserMainForm.errors)
    
    else:
        form = UserMainForm()

    return render(request, 'user/register.html', context= {'RegisterForm':form})

def LoginView(request):
    if request.method == "POST":
        form = UserLoginForm(data= request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username= username, password= password)

            if user:
                login(request, user)
                return redirect('index')
            
            else:
                return redirect('index')
        
        else:
            print("form validation or login error")

    else:
        form = UserLoginForm()

    return render(request,"user/login.html", context= {"LoginForm":form})

def LogoutView(request):
    logout(request)
    return redirect('index')

