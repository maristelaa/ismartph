from . import views
from django.urls import path

urlpatterns = [
    path('', views.logIn, name='logIn'),
    #path('dashboard', views.dashboard, name='dashboard'),
    #path('logout/', views.logout_view, name='logout'),
    #path('register_user/', views.registerUser, name="register_user"),
    #path('register_user/register/', views.register, name='register'),
    path('forgot_pass/', views.forgot_pass, name="forgot_pass"),
    path('forgot_pass/password_reset/', views.password_reset, name='password_reset'),
    path('crops',views.crops, name='crops'),
    path('home', views.home, name='home'),
    path('mycrop', views.mycrop, name='mycrop'),


    #try lang
    #path('index', views.signIn, name='index'),

    path('dashboard', views.postSign, name='postSign'),
    
    path('login_required', views.login_required_view, name='login_required'),

    path('signOut', views.signOut, name='signout'),
    path('logout_required', views.logout_required_view, name='logout_required'),

    path('signup', views.signUp, name="signup"),
    path('postsignup', views.postsignup, name="postsignup"),
    
    path('fetch_data', views.fetch_data, name="fetch"),
    

]