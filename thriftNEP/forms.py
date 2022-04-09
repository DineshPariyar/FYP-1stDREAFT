import email
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


class PasswordForgetForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"enter the email you used."
    }))

    def clean_email(self):
        e=self.cleaned_data.get("email")
        if Seller.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError("seller with this user doesnot exist")
        
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password") 
    confirm_new_password= forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password") 

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Password did not match!")
        return confirm_new_password




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