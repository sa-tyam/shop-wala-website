"""ShopWala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from . import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPage, name='landing_page'),
    path('home/', views.SellerHome, name='seller_home'),
    path('sign_out/', views.SignOut, name='sign_out'),
    path('phoneVerify/', views.PostPhoneVerify, name='phoneVerify'),
    path('logged_in/', views.LoggedIn, name='logged_in'),
    path('postPhoneVerify/', views.UserOtpVerification, name='postPhoneVerify'),
    path('seller_products/', views.SellerProducts, name='seller_products'),
    url(r"seller_product_detail/$",views.SellerProductDetails, name="seller_product_detail"),
    url(r"buyer_bag/$",views.BuyerBag, name="buyer_bag"),
    url(r"buyer_orders/$",views.BuyerOrders, name="buyer_orders"),
    url(r"buyer_order_details/$",views.BuyerOrderDetails, name="buyer_order_details"),
    url(r"add_to_bag/$",views.AddToBag, name="add_to_bag"),
    url(r"buy_now/$",views.BuyNow, name="buy_now"),
    url(r"place_order/$",views.PlaceOrder, name="place_order"),
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
