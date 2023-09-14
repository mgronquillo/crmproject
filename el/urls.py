from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='el-home'),
    path('products/', views.products, name='el-products'),
    path('register/', views.registerPage, name='el-register'),
    path('login/', views.loginPage, name='el-login'),
    path('logout/', views.logoutPage, name='el-logout'),
    path('customer/<str:pk>', views.customer, name='el-customer'),
    path('create_customer/', views.createCustomer, name='el-create_customer'),
    path('update_customer/<str:pk>', views.updateCustomer, name='el-update_customer'),
    path('delete_customer/<str:pk>', views.deleteCustomer, name='el-delete_customer'),
    path('create_order/<str:pk>', views.createOrder, name='el-create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='el-update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='el-delete_order'),
]