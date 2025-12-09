from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('', views.home , name = 'home' ),
    path('signup/', views.sign_up , name = 'signup' ),
    path('login/', views.log_in , name = 'login' ),
    path('logout/', views.log_out , name = 'logout' ),
    path('profile/', views.profile , name = 'profile' ),
    path('create_poll/', views.create_poll , name = 'create' ),
]