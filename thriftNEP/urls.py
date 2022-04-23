from django.urls import URLPattern, path
from .views import *


app_name = "thriftNEP"
urlpatterns=[
    path("",HomeView.as_view(), name="home"),
    path("help/",HelpView.as_view(), name="help"),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:slug>", ProductDetailView.as_view(), name="productdetail"),

    # path("register/",SellerRegistrationView.as_view(), name="sellerregistration"),
    path("register/",SellerRegistrationView, name="sellerregistration"),


    path("login/",SellerLoginView.as_view(), name="sellerlogin"),
    path("logout/",SellerLogoutView.as_view(), name="sellerlogout"),
    path("forget-password/",PasswordForgetView.as_view(),name="forgotpw"),
    path("password-reset/<email>/<token>/", PasswordResetView.as_view(), name="passwordreset"),


    

    path("profile/",SellerProfileView.as_view(), name="sellerprofile"),
    path("product-create/", SellerProductCreateView.as_view(), name="sellerproductcreate"),
    path("product-<pro_id>-sold/", SellerProductSoldView.as_view(), name="sellerproductsold"),
    path("search/", SearchView.as_view(), name="search"),
    path('searchItem/',search,name='searchItem'),
    path('delete_product/<int:id>/',delete_product,name="delete_product"),


    # path("seller-product/list/",SellerProductListView.as_view(), name="sellerproductlistview "),
]