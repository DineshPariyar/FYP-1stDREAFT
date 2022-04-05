from django.urls import URLPattern, path
from .views import *


app_name = "thriftNEP"
urlpatterns=[
    path("",HomeView.as_view(), name="home"),
    path("help/",HelpView.as_view(), name="help"),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:slug>", ProductDetailView.as_view(), name="productdetail"),

    path("register/",SellerRegistrationView.as_view(), name="sellerregistration"),

    path("login/",SellerLoginView.as_view(), name="sellerlogin"),
    path("logout/",SellerLogoutView.as_view(), name="sellerlogout"),
    

    path("profile/",SellerProfileView.as_view(), name="sellerprofile"),
    path("product-create/", SellerProductCreateView.as_view(), name="sellerproductcreate"),
    path("product-<pro_id>-sold/", SellerProductSoldView.as_view(), name="sellerproductsold"),
    path("search/", SearchView.as_view(), name="search"),



    path("admin-login/",AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home",AdminHomeView.as_view(),name="adminhome"),


    # path("seller-product/list/",SellerProductListView.as_view(), name="sellerproductlistview "),
]