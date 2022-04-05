from django import forms
from .models import Product, Seller
from django.contrib.auth.models import User


class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model=Seller
        fields=["username","password","email","full_name", "address"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Seller with this Username already exist!!  Please use other Username")
        return uname

class SellerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class SellerProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title",  "slug", "category", "image", "price", "description", "return_policy"]