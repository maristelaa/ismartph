from functools import wraps
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from requests.exceptions import HTTPError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse    
from django.contrib import messages
from .forms import PasswordResetForm
from django.urls import reverse
import pyrebase
import json

config = {

    "apiKey": "AIzaSyDaS4IRYzvj2DwKCnn2qWeQCSLc6pOtzmM",
    "authDomain": "ismartph.firebaseapp.com",
    "databaseURL": "https://ismartph-default-rtdb.firebaseio.com",
    "projectId": "ismartph",
    "storageBucket": "ismartph.appspot.com",
    "messagingSenderId": "387773292296",
    "appId": "1:387773292296:web:20553e9f8e46e2b16b16bd",
    "serviceAccount": "C:\\Users\\angie\\OneDrive\\Desktop\\ismartph-firebase-adminsdk-5xxlu-35a004fa8f.json",
}

firebase  = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


def logIn(request):
    return render(request, "ismartproj/logIn.html")

# Helper function to get user data from Firebase
def get_user_data(request, email, password):
    try:
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # User is authenticated
            uid = user.uid  # Assuming the Firebase UID is stored in the user object
            user_data = database.child("users").child(uid).child("useraccount").get().val()
            return user_data
        else:
            # User is not authenticated; redirect to the login page
            messages.error(request, 'Please log in to access this page.')
            return redirect('logIn')  # Make sure 'logIn' is the correct URL name for your login page

    except:
        raise Exception("Invalid Email or Password")

def dashboard(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    try: 
        user = firebase.auth().sign_in_with_email_and_password(email, password)

        # Get the user's UID
        uid = user['localId']
        
        # Retrieve the user's fName from Firebase
        user_data = database.child("users").child(uid).child("useraccount").get().val()
        fName = user_data.get("fName", "")
        lName = user_data.get("lName", "")

        # Store the uid and idToken in the session
        session_data = {
            'uid': uid,
            'idToken': user['idToken'],
        }
        request.session.update(session_data)

        return render(request, 'ismartproj/home.html', {'e': email, 'fName': fName, 'lName': lName})
    
    except:
        message = "Invalid Email or Password"
        return render(request, "ismartproj/logIn.html", {"messg": message})
    
#new changes
def logout_view(request):
    # Log out from Firebase (if the user is logged in)
    uid = request.session.get('uid')
    if uid:
        firebase.auth().signOut()

    # Clear the Django session
    try:
        del request.session['uid']
    except KeyError:
        pass

    # Redirect to the login page
    return redirect('logIn')

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

@login_required(login_url='logIn')        
def crops(request):
    try:
        # Check if the user is authenticated
        if 'uid' not in request.session:
            raise KeyError("User not authenticated")
        
        elif 'uid' in request.session:
            return redirect('crops')
        
        # Retrieve the uid from the session
        uid = request.session['uid']

        # Retrieve the user's fName from Firebase using the uid
        user_data = database.child('users').child(uid).child('useraccount').get().val()
        fName = user_data.get("fName", "")

        return render(request, 'ismartproj/mycrops.html', {'fName': fName})
    except KeyError:
        message = "User Logged Out, Kindly Log In second"
        return render(request, "ismartproj/logIn.html", {"messg": message})
    except Exception as e:
        # Handle any other exceptions that may occur
        error_message = str(e)
        return render(request, "ismartproj/logIn.html", {"messg": error_message})



@login_required(login_url='logIn')        
#new changes
def home(request):
    try:
        # Check if the user is authenticated
        if 'uid' not in request.session:
            raise KeyError("User not authenticated")
        
        # Retrieve the uid from the session
        uid = request.session['uid']

        # Retrieve the user's fName from Firebase using the uid
        user_data = database.child('users').child(uid).child('useraccount').get().val()
        fName = user_data.get("fName", "")
        lName = user_data.get("lName", "")

        return render(request, 'ismartproj/home.html', {'fName': fName, 'lName': lName})
    except KeyError:
        message = "User Logged Out, Kindly Log In second"
        return render(request, "ismartproj/logIn.html", {"messg": message})
    except Exception as e:
        # Handle any other exceptions that may occur
        error_message = str(e)
        return render(request, "ismartproj/logIn.html", {"messg": error_message})