from django.urls import path
from . import views

urlpatterns = [
    path ('', views.index, name="index"),
    path ('registration/', views.registration, name="registration"),
    path ('login/', views.loginPage, name="login"),
    path ('logout/', views.logoutUser, name="logout"),

    path ('customers/', views.customers, name="customers"),
    path ('customers/<str:pk>/', views.customers, name="customers"),

    path ('products/', views.products, name="products"),

    path ('create_order/<str:pk>/', views.createOrder, name="create_order"),  
    path ('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path ('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"), 
]