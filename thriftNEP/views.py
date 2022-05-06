from unicodedata import category
from django.views.generic import  View, TemplateView,CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.models import User, auth #new
from django.core.mail import send_mail
from itertools import chain, product
from thriftNEP.models import Product   #its imported bcz of class based function 
from multiprocessing import context
from msilib.schema import ListView
from django.conf import settings
from django.db.models import Q
from genericpath import exists
from email.mime import image
from urllib import request, response
from turtle import title
from cgitb import text
from .models import *
from .forms import *

# Create your views here.

class HomeView(TemplateView):  #here TemplateView is being inheritated and all the properties of ttemplateView will be aailable in the defined class. 
    template_name= "home.html" #-->eg::-required_attribute name ="templates.html"
                    #function for sending backend details of product from database to template.
    def get_context_data(self, **kwargs): # this is sthe fundamental style of writing get context data
        context = super().get_context_data(**kwargs)
        #what doe this does is whenever we add some context it express in the frontend.
        all_products = Product.objects.all().order_by("-id")
        paginator = Paginator(all_products, 6)
        page_number = self.request.GET.get('page')
        product_list=paginator.get_page(page_number)
        context['product_list'] = product_list
        context['category'] = Category.objects.all()
        return context


def filter_page(request,query):# we use this for the listing of the category list dyanamically.
    context = {'product_list':Product.objects.filter(category=Category.objects.get(title=query)),'category' :Category.objects.all(),'Name':query}
    return render(request,"filter.html",context)



class AllProductsView(TemplateView): # in this section the function is writeen to show al the products in the home page.
    template_name="allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories']=Category.objects.all()
        context['category'] = Category.objects.all()

        return context

class ProductDetailView(TemplateView):
    template_name="productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        context['product']=product
        context['category'] = Category.objects.all()

        return context


# class SellerRegistrationView(CreateView):
#     template_name="registration11.html"
#     form_class = SellerRegistrationForm
#     success_url=reverse_lazy("thriftNEP:home")

#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         email = form.cleaned_data.get("email")
#         user=User.objects.create_user(username, email, password)
#         form.instance.user=user
#         login(self.request, user)
#         return super().form_valid(form)


def SellerRegistrationView(request): 
    if request.method=="POST":
        username = request.POST["user"]
        print("weeffffffffffffffffff")
        print(username)
        email=request.POST["email"]
        password=request.POST["password"]
        full_name=request.POST["full_name"]
        address=request.POST["address"]
        number=request.POST["number"]
        # context['category'] = Category.objects.all()

        user=User.objects.create_user(username=username,email=email,password=password)
        user.first_name = full_name
        user.save();
        seller=Seller(user=user,full_name=full_name,address=address,mobile=number)
        seller.save();
        print('user created')
        return redirect('/')
    else:
        return render(request,"registerTest.html")


class SellerLoginView(FormView):
    template_name="sellerlogin.html"
    form_class = SellerLoginForm
    success_url=reverse_lazy("thriftNEP:home")

    def form_valid(self,form):
        uname=form.cleaned_data.get("username")
        pword =form.cleaned_data["password"]
        usr=authenticate(username=uname, password=pword)
        if usr is not None and Seller.objects.filter(user=usr).exists() :
            login(self.request, usr)
        else:
            return render(self.request,self.template_name, {"form": self.form_class, "error":"Invalid Username and Password"})

        # context['category'] = Category.objects.all()

        return super().form_valid(form)


class PasswordForgetView(FormView):
    template_name="forgotpw.html"
    form_class = PasswordForgetForm
    success_url="/forget-password/?m=s"

    def form_valid(self, form): 
        #get email from user 
        email=form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        #get seller and then user
        seller=Seller.objects.get(user__email=email)
        user=seller.user
        #send mail to the user with email.
        text_content= 'Please Click the link to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link from thriftNEP',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)
####################################################################################

class PasswordResetView(FormView):
    template_name="passwordreset.html"
    form_class = PasswordResetForm
    success_url="/login/"


    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("thriftNEP:forgotpw")+ "?m=e")  
        return super().dispatch(request, *args, **kwargs)
            
        
    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)



##############################################################################

class SellerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.seller = request.user.seller
        except Exception as e:
            print(e)
            return redirect("thriftNEP:sellerlogin")
        # context['category'] = Category.objects.all()
        return super().dispatch(request, *args, **kwargs)



class SellerLogoutView(SellerMixin, View):
    def get(self,request):
        logout(request)
        
        return redirect("thriftNEP:home")

class HelpView(TemplateView):
    template_name= "help.html"

    def get_context_data(self, **kwargs):
            context =super().get_context_data(**kwargs)
            context['category'] = Category.objects.all()
            return context




class SellerProfileView(SellerMixin, TemplateView):
    template_name="sellerprofile.html"

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['seller'] = self.seller
        context["product_list"] = Product.objects.filter(seller=self.seller).order_by("-id")
        # context['category'] = Category.objects.all()
        return context
        

class SellerProductCreateView(SellerMixin, CreateView):
    template_name = "sellerproductcreate.html"
    form_class = SellerProductCreateForm
    success_url = reverse_lazy("thriftNEP:sellerprofile")
    # context['category'] = Category.objects.all()

    def form_valid(self, form):
        form.instance.seller = self.seller
        form.instance.seller_number = self.seller.mobile or "9898989898"
        form.instance.seller_address = self.seller.address
        form.instance.status = "On Sale"

        form.save()
        # more_images=self.request.FILES.getlist("more_images")
        # for i in more_images:
        #     ProductImages.objects.create(product=p, image=i)

        # context['category'] = Category.objects.all()
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

def delete_product(request,id):
    obj = Product.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/profile/')


# class SellerProductListView(SellerRequiredMixin, ListView):
#     template_name = "sellerproductlist.html"
#     queryset =Product.objects.all().order_by("-id")
#     context_object_name ="allproducts"
 


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        search_list = Product.objects.filter(Q(title__icontains=kw)  | Q(description__icontains=kw) | Q(return_policy__icontains=kw))
        paginator = Paginator(search_list, 9)
        page_number = self.request.GET.get('page')
        print("Dinesh don")
        print(search_list)
        search_list=paginator.get_page(page_number)
        context["search_list"]= search_list
        print("Dinesh don")
        print(search_list)
        context['category'] = Category.objects.all()
        return context


#  all_products = Product.objects.all().order_by("-id")
#         paginator = Paginator(all_products, 9)
#         page_number = self.request.GET.get('page')
#         product_list=paginator.get_page(page_number)
#         context['product_list'] = product_list
#         return context



def search(request):
    kw = request.GET.get("keyword") 
    if kw is None:
        kw = request.COOKIES.get('kw')
  
    search_list = Product.objects.filter(Q(title__icontains=kw)  | Q(description__icontains=kw) | Q(return_policy__icontains=kw))  # fetching all post objects from database
    p = Paginator(search_list, 6)  
    page_number = request.GET.get('page')
    try:
        search_list = p.get_page(page_number)  
    except PageNotAnInteger:
        search_list = p.page(1)
    except EmptyPage:
        search_list = p.page(p.num_pages)
    context = {'search_list': search_list,'key':kw}
    response = render(request, 'search.html', context)
    response.set_cookie('kw', kw, max_age = None, expires = None)
    context['category'] = Category.objects.all()

    return response