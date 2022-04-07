from distutils.command.upload import upload
import email
from tkinter import CASCADE
from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile= models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name= models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


PRODUCT_STATUS = (
    ("On Sale", "On Sale"),
    ("Sold", "Sold"),
    ("Disabled", "Disabled"),
)

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    price = models.PositiveIntegerField()
    description = models.TextField()
    return_policy=models.CharField(max_length=200, null=True, blank=True)
    seller_number=models.CharField(max_length=10)
    seller_address=models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title
