from django import forms
from .models import Product, Seller
from django.contrib.auth.models import User


class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    class Meta:
        model=Seller
        fields=["username","password","email","full_name", "address","mobile"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Seller with this Username already exist!!  Please use other Username")
        return uname

class SellerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class SellerProductCreateForm(forms.ModelForm):
    more_images= forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple":True
    }))
    class Meta:
        model = Product
        fields = ["title",  "slug", "category", "image", "price", "description", "return_policy"]

        widgets ={
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enterthe product Title"
            }),

            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enterthe unique slug"
            }),


            "category": forms.Select(attrs={
                "class": "form-control",
            }),


            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enterthe product price"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "description of  product",
                "rows":5
            }),

            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enterthe product Title"
            }),
        }