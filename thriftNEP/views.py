from genericpath import exists
from itertools import chain, product
from msilib.schema import ListView
from multiprocessing import context
from turtle import title
from urllib import request
from django.http import HttpResponseRedirect
from django.views.generic import  View, TemplateView,CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from .forms import *
from thriftNEP.models import Product   #its imported bcz of class based function 
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from .models import *

# Create your views here.

class HomeView(TemplateView):  #here TemplateView is being inheritated and all the properties of ttemplateView will be aailable in the defined class. 
    template_name= "home.html" #-->eg::-required_attribute name ="templates.html"
                    #function for sending backend details of product from database to template.
    def get_context_data(self, **kwargs): # this is sthe fundamental style of writing get context data
        context = super().get_context_data(**kwargs)
        #what doe this does is whenever we add some context it express in the frontend.
        all_products = Product.objects.all().order_by("-id")
        paginator = Paginator(all_products, 4)
        page_number = self.request.GET.get('page')
        product_list=paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class AllProductsView(TemplateView):
    template_name="allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories']=Category.objects.all()
        return context

class ProductDetailView(TemplateView):
    template_name="productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        context['product']=product
        return context


class SellerRegistrationView(CreateView):
    template_name="registration.html"
    form_class = SellerRegistrationForm
    success_url=reverse_lazy("thriftNEP:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user=User.objects.create_user(username, email, password)
        form.instance.user=user
        login(self.request, user)
        return super().form_valid(form)



class SellerLoginView(FormView):
    template_name="sellerlogin.html"
    form_class = SellerLoginForm
    success_url=reverse_lazy("thriftNEP:home")

    def form_valid(self,form):
        uname=form.cleaned_data.get("username")
        pword =form.cleaned_data["password"]
        usr=authenticate(username=uname, password=pword)
        if usr is not None and Seller.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name, {"form": self.form_class, "error":"Invalid Username and Password"})

        return super().form_valid(form)


class SellerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.seller = request.user.seller
        except Exception as e:
            print(e)
            return redirect("thriftNEP:sellerlogin")
        return super().dispatch(request, *args, **kwargs)


class SellerLogoutView(SellerMixin, View):
    def get(self,request):
        logout(request)
        return redirect("thriftNEP:home")

class HelpView(TemplateView):
    template_name= "help.html"




class SellerProfileView(SellerMixin, TemplateView):
    template_name="sellerprofile.html"

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['seller'] = self.seller
        context["product_list"] = Product.objects.filter(seller=self.seller).order_by("-id")
        return context
        

class SellerProductCreateView(SellerMixin, CreateView):
    template_name = "sellerproductcreate.html"
    form_class = SellerProductCreateForm
    success_url = reverse_lazy("thriftNEP:sellerprofile")

    def form_valid(self, form):
        form.instance.seller = self.seller
        form.instance.seller_number = self.seller.mobile or "9898989898"
        form.instance.seller_address = self.seller.address
        form.instance.status = "On Sale"
        return super().form_valid(form)


class SellerProductSoldView(SellerMixin, TemplateView):
    template_name = "sellerproductsold.html"

    def post(self, request, pro_id):
        try:
            product_obj = Product.objects.get(id=pro_id)
            product_obj.status = "Sold"
            product_obj.save()
        except Exception as e:
            print(e)
            return redirect("thriftNEP:sellerprofile")
        return redirect("thriftNEP:sellerprofile")


# class SellerProductListView(SellerRequiredMixin, ListView):
#     template_name = "sellerproductlist.html"
#     queryset =Product.objects.all().order_by("-id")
#     context_object_name ="allproducts"
 


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(title__icontains=kw)  | Q(description__icontains=kw) | Q(return_policy__icontains=kw))
        context["results"]= results
        print(results)
        return context







#admin login
class AdminLoginView(FormView):
    template_name= "admin/adminlogin.html"
    form_class=SellerLoginForm
    success_url=reverse_lazy("thriftNEP:adminhome")

    def form_valid(self, form):
        uname=form.cleaned_data.get("username")
        pword =form.cleaned_data["password"]
        usr=authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name, {"form": self.form_class, "error":"Invalid Username and Password"})

        return super().form_valid(form)



class AdminHomeView(TemplateView):
    template_name="admin/adminhome.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user= request.user).exists():
            pass
        else:
            return redirect("/admin-login/")


        return super().dispatch(request, *args, **kwargs)


def delete_product(request,id):
    obj = Product.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/profile/')