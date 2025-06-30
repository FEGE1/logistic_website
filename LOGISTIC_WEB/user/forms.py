from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserMainForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirmPassword=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')
    
    def clean(self):
        username=self.cleaned_data.get("username")
        email=self.cleaned_data.get("email")
        password=self.cleaned_data.get("password")
        confirmPassword=self.cleaned_data.get("confirmPassword")

        if password and confirmPassword and password != confirmPassword:
            raise forms.ValidationError("Password Unmatched!")
        else:
            values={
                "username":username,
                "password":password,
                "email":email,
            }
            return values
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length= 50, label= "Username")
    password = forms.CharField(max_length= 50, label= "Password", widget= forms.PasswordInput)

    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
            
        if authenticate(username=username, password=password):
            values={
            "username":username,
            "password":password,
            }
            return values

        else:
            raise forms.ValidationError("Kullanıcı adı veya şifre hatalı.")