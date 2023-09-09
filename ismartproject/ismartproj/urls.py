from . import views
from django.urls import path

urlpatterns = [
    path('', views.logIn, name='logIn'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.logout_view, name="logout"),
    path('register_user/', views.registerUser, name="register_user"),
    path('register_user/register/', views.register, name='register'),
    path('forgot_pass/', views.forgot_pass, name="forgot_pass"),
    path('forgot_pass/password_reset/', views.password_reset, name='password_reset'),
    path('mycrops/',views.mycrops, name='mycrops'),
    path('crops/',views.crops, name='crops'),
    path('dashboard', views.home, name='home'),
]