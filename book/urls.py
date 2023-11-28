"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book_admin import views

# from django.conf.urls import url
from django.contrib import admin
from django.urls import include, re_path as url

from book_admin.views import HomeView, ChartData

urlpatterns = [

    url(r'home', HomeView.as_view(), name='home'),

    url(r'^api/chart/data/$', ChartData.as_view(), name='api-data'),

    path('admin/', admin.site.urls),
    path('show/', views.show),
    path('area/', views.show_area),
    path('user/', views.show_user),
    path('category/', views.show_category),
    path('sub_category/', views.show_sub_category),
    path('language/', views.show_language),
    path('book/', views.show_book),
    path('order/', views.show_order),
    path('order_detail/', views.show_order_detail),
    path('wishlist/', views.show_wishlist),
    path('feedback/', views.show_feedback),
    path('d_area/<int:aid>', views.destroy_area),
    path('update_area/<int:ai>', views.update_area),
    path('d_language/<int:lid>', views.destroy_language),
    path('update_language/<int:li>', views.update_language),
    path('d_book/<int:bid>', views.destroy_book),
    path('update_book/<int:bi>', views.update_book),
    path('update_image/<int:bi>', views.update_image),
    path('d_category/<int:cid>', views.destroy_category),
    path('update_category/<int:ci>', views.update_category),
    path('d_sub_category/<int:sid>', views.destroy_sub_category),
    path('update_sub_category/<int:si>', views.update_sub_category),
    path('d_feedback/<int:fid>', views.destroy_feedback),
    path('d_wishlist/<int:wid>', views.destroy_wishlist),
    path('d_user/<int:uid>', views.destroy_user),
    path('dashboard/', views.show_dashboard),
    path('login/', views.admin_login),
    path('logout/', views.admin_logout),
    path('ai/', views.insert_Area),
    path('ci/', views.insert_Category),
    path('si/', views.insert_Sub_Category),
    path('li/', views.insert_Language),
    path('bi/', views.insert_Book),
    path('forgot_password/', views.forgot),
    path('send_otp/', views.sendotp),
    path('set_password/', views.set_password),
    path('od_report1/', views.order_report1),
    path('od_report2/', views.order_report2),
    path('od_report3/', views.order_report3),
    path('od_report4/', views.order_report4),
    path('od_report5/', views.order_report5),
    path('accept/<int:id>', views.accept_order),
    path('reject/<int:id>', views.reject_order),
    path('profile/', views.show_profile),
    path('update_pass/', views.update_pass),


    path('c/', include('book_customer.customer_urls'))
]
