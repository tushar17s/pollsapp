from django.contrib import admin
from django.urls import path , include
from . import views
from . views import PollListAPIView , PollDetailAPIView , ResultAPIView
urlpatterns = [
    path('', views.home , name = 'home' ),
    path('signup/', views.sign_up , name = 'signup' ),
    path('login/', views.log_in , name = 'login' ),
    path('logout/', views.log_out , name = 'logout' ),
    path('dashboard/', views.dashboard , name = 'dashboard' ),
    path('medashboard/', views.medashboard , name = 'medashboard' ),
    path('create_poll/', views.create_poll , name = 'create' ),
    path('voting/<int:poll_id>/<int:opt_id>/', views.voting , name = 'voting' ),
    path('detail/<int:poll_id>/', views.poll_detail , name = 'detail' ),
    path('comment/<int:poll_id>/', views.comment_func , name = 'comment' ),
    path('hide/<int:comment_id>/<int:poll_id>/', views.hide_comment , name = 'hide_comment' ),
    path('edit/<int:comment_id>/<int:poll_id>/', views.edit_comment , name = 'edit_comment' ),
    path('undo/<int:poll_id>/', views.undo_vote , name = 'undo' ),
    path('delete/<int:poll_id>/', views.delete_poll , name = 'delete_poll' ),
    path('api/polls/',PollListAPIView.as_view(),name="api_view"),
    path('api/polls/<int:poll_id>/',PollDetailAPIView.as_view(),name="apidetail_view"),
    path('api/polls/<int:poll_id>/results',ResultAPIView.as_view(),name="apiresult_view"),
]
