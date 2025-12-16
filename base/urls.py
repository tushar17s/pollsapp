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
    path('voting/<int:poll_id>/<int:opt_id>/', views.voting , name = 'voting' ),
    path('detail/<int:poll_id>/', views.poll_detail , name = 'detail' ),
    path('comment/<int:poll_id>/', views.comment_func , name = 'comment' ),
    path('hide/<int:comment_id>/<int:poll_id>/', views.hide_comment , name = 'hide_comment' ),
]
