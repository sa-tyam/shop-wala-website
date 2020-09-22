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
    path('', views.SellerHome, name='seller_home'),
    path('signin/', views.SignIn, name='signin'),
    path('signup/', views.SignUp, name='signup'),
    path('post_signup/', views.PostSignUp, name='post_signup'),
    path('post_signin/', views.PostSignIn, name='post_signin'),
    path('seller_categories/', views.SellerCategories, name='seller_categories'),
    url(r"seller_category_detail/$",views.SellerCategoriesDetails, name="seller_category_detail"),
    url(r"buyer_bag/$",views.BuyerBag, name="buyer_bag"),
    url(r"buyer_orders/$",views.BuyerOrders, name="buyer_orders"),
    url(r"add_to_bag/$",views.AddToBag, name="add_to_bag"),
    url(r"buy_now/$",views.BuyNow, name="buy_now"),
    url(r"place_order/$",views.PlaceOrder, name="place_order"),
] +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
