from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse    
from django.contrib import messages
from .forms import PasswordResetForm
import pyrebase

config = {

    "apiKey": "AIzaSyDaS4IRYzvj2DwKCnn2qWeQCSLc6pOtzmM",
    "authDomain": "ismartph.firebaseapp.com",
    "databaseURL": "https://ismartph-default-rtdb.firebaseio.com",
    "projectId": "ismartph",
    "storageBucket": "ismartph.appspot.com",
    "messagingSenderId": "387773292296",
    "appId": "1:387773292296:web:20553e9f8e46e2b16b16bd",

}

firebase  = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


def logIn(request):
    return render(request, "ismartproj/logIn.html")

def dashboard(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try: 
        user = auth.sign_in_with_email_and_password(email, password)

        # Get the user's UID
        uid = user['localId']
        
        # Retrieve the user's fName from Firebase
        user_data = database.child("users").child(uid).child("useraccount").get().val()
        fName = user_data.get("fName", "")

        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        
        return render(request, 'ismartproj/home.html', {'fName': fName})
    
    except:
        message = "Invalid Emaill or Password"
        return render(request,"ismartproj/logIn.html", {"messg":message})
   

def logout_view(request):
    
    logout(request)    
    return render(request, 'ismartproj/logIn.html')

def registerUser(request):
    return render(request, 'ismartproj/register_user.html')

def register(request):

    if request.method == 'POST':
        
        fName = request.POST.get('fName')
        mName = request.POST.get('mName')
        lName = request.POST.get('lName')
        sName = request.POST.get('sName')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        

        user = auth.create_user_with_email_and_password(email_address,password)

        uid = user['localId']

        data={"fName":fName,"mName":mName,"lName":lName,"sName":sName,"status":"1"}

        database.child("users").child(uid).child("useraccount").set(data)

        return redirect('logIn')
    
    return render(request,"ismartproj/register_user.html")

def forgot_pass(request):
    return render(request, 'ismartproj/forgot_pass.html')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                auth.send_password_reset_email(email)  # Placeholder for Firebase function
                messages.success(request, 'We have already sent a link to your account to reset your password, you can now check your email.')
            except pyrebase.pyrebase.HTTPError as e:
                error_message = e.args[1]['error']['message']
                messages.error(request, f'Error sending password reset email: {error_message}')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again later.')

    else:
        form = PasswordResetForm()
    
    return render(request, 'ismartproj/password_reset.html', {'form': form})



def crops(request):
    return render(request, 'ismartproj/mycrops.html')


def home(request):
    return render(request, 'ismartproj/home.html')