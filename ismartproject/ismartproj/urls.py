from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_view, name='logIn'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('register_user/', views.registerUser, name="register_user"),
    path('register_user/register/', views.register, name='register'),
    path('forgot_pass/', views.forgot_pass, name="forgot_pass"),
    path('forgot_pass/password_reset/', views.password_reset, name='password_reset'),
    path('crops',views.crops, name='crops'),
    path('home', views.home, name='home'),
]