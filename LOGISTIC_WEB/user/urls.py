from django.contrib import admin
from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

app_name = "user"

urlpatterns = [
    path('register/', views.RegisterView, name= "register"),
    path('login/', views.LoginView, name= "login"),
    path('logout/', views.LogoutView, name= "logout"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)