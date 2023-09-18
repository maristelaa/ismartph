from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib import auth 
from django.contrib.auth.models import User
from requests.exceptions import HTTPError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse    
from django.contrib import messages
from .forms import PasswordResetForm
from .models import CustomUser
from django.http import HttpResponse
from django.urls import reverse
import pyrebase
import json
import firebase_admin
from firebase_admin import auth

config = {

    "apiKey": "AIzaSyDRo3n2Vau04OzvSoi6kPjSH0hdwDvmXBg",
    "authDomain": "smart-6aa8f.firebaseapp.com",
    "databaseURL": "https://smart-6aa8f-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "smart-6aa8f",
    "storageBucket": "smart-6aa8f.appspot.com",
    "messagingSenderId": "940651613138",
    "appId": "1:940651613138:web:f27e20eb6140e0d7dc160b",
    "serviceAccount": "C:\\Users\\angie\\OneDrive\\Desktop\\smart-6aa8f-firebase-adminsdk-xxkfg-27def7bfeb.json",
}

firebase  = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def logIn(request):
    return render(request, "ismartproj/logIn.html")

# Helper function to get user data from Firebase
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Attempt Firebase authentication
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            uid = user['localId']

            # Retrieve user data from Firebase
            user_data = database.child("users").child(uid).child("useraccount").get().val()
            fName = user_data.get("fName", "")
            lName = user_data.get("lName", "")

            # Store the uid and idToken in the session
            session_data = {
                'uid': uid,
                'localId': user['localId'],
            }
            
            request.session.update(session_data)

            return render(request, 'ismartproj/home.html', {'e': email, 'fName': fName, 'lName': lName})
        
        except:
            # Both Firebase and Django authentication failed
            message = "Invalid Email or Password"
            return render(request, "ismartproj/logIn.html", {"messg": message})

    else:
        # Render the login form
        return render(request, "ismartproj/logIn.html")

#def dashboard(request):
    try:
        # Check if the user is authenticated through Firebase
        if 'uid' in request.session:
            uid = request.session['uid']
            user_data = database.child("users").child(uid).child("useraccount").get().val()
            fName = user_data.get("fName", "")
            lName = user_data.get("lName", "")
            return render(request, "ismartproj/home.html", {'e': request.user.email, 'fName': fName, 'lName': lName})

        # Neither Firebase nor Django authentication succeeded
        message = "User not Authenticated"
        return render(request, "ismartproj/logIn.html", {"messg": message})

    except KeyError:
        # message = "User Logged Out, Kindly Log In again"
        return render(request, "ismartproj/logIn.html", {"messg": message})

    except Exception as e:
        # Handle any other exceptions that may occur
        error_message = str(e)
        return render(request, "ismartproj/logIn.html", {"messg": error_message})


def logout_view(request):
    # Log out from Firebase (if the user is logged in)
    if 'uid' in request.session:
        # If using Firebase authentication, clear the user's session data
        del request.session['uid']
        del request.session['localId']

    # Redirect to the login page or any other desired URL
    return redirect('logIn')


def registerUser(request):
    return render(request, 'ismartproj/register_user.html')

def register(request):
    if request.method == 'POST':
        fName = request.POST.get('fName')
        mName = request.POST.get('mName')
        lName = request.POST.get('lName')
        sName = request.POST.get('sName')
        username = request.POST.get('username')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        try:
            # Create a new CustomUser instance and save it to the Django database
            user = CustomUser.objects.create_user(
                username=username,
                email=email_address,
                password=password,
                fName=fName,
                mName=mName,
                lName=lName,
                sName=sName,
                # Add other fields as needed
            )
            # Log in the user
            login(request, user)

            # Add a success message
            messages.success(request, "Registration successful!")

            # Save data to Firebase
            user = authe.create_user_with_email_and_password(email_address, password)
            uid = user['localId']
            data = {
                "fName": fName,
                "mName": mName,
                "lName": lName,
                "sName": sName,
                "username": username,
                "status": "1",
            }
            database.child("users").child(uid).child("useraccount").set(data)

        except Exception as e:
            # Registration failed, add an error message
            message = "Registration failed: " + str(e)
            messages.error(request, message)

        # After creating the user in Django and Firebase, you can redirect to the desired page.
        return redirect('logIn')  # Change this to the appropriate redirect URL

    return render(request, "ismartproj/logIn.html")


def forgot_pass(request):
    return render(request, 'ismartproj/forgot_pass.html')

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                authe.send_password_reset_email(email)  # Placeholder for Firebase function
                messages.success(request, 'We have already sent a link to your account to reset your password, you can now check your email.')
            except pyrebase.pyrebase.HTTPError as e:
                error_message = e.args[1]['error']['message']
                messages.error(request, f'Error sending password reset email: {error_message}')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again later.')

    else:
        form = PasswordResetForm()
    
    return render(request, 'ismartproj/password_reset.html', {'form': form})

def home(request):
    return render(request, "ismartproj/home.html")




def mycrop(request):
    return render(request, "ismartproj/mycrop.html")


#try

def signIn(request):
    return render(request, "ismartproj/index.html")


def login_required_view(request):
    return HttpResponse("Enter your credentials first.")

def postSign(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('pass')

        try:
            user = authe.sign_in_with_email_and_password(email, passw)

            # Get the User UID
            user_uid = user['localId']

            # Store the User UID in the session
            request.session['uid'] = str(user_uid) 

            # Print the session variable for debugging
            print("Firebase UID stored in session:", user_uid)

            # Get the previously stored 'current_path' (if it exists)
            current_path = request.session.get('current_path')

            if current_path:
                # Redirect to the stored path
                return redirect(current_path)
            else:
                # If there's no stored path, redirect to the home page
                return render(request, "ismartproj/home.html", {"e": email})
        except Exception as e:
            # Print the exception for debugging
            print("Exception in postSign:", str(e))
            message = "Invalid Email or Password"
            return render(request, "ismartproj/index.html", {"messg": message})
    else:
        # Handle GET request (render the login page)
        return render(request, "ismartproj/index.html")




def logout_required_view(request):
    response = HttpResponse("Kindly logout your account first.")


def signOut(request):
    # Perform logout
    auth.logout(request)

    # Get the stored path from the session (if it exists)
    stored_path = request.session.get('current_path')

    if stored_path:
        # Clear the 'current_path' from the session
        del request.session['current_path']

        # Redirect to the stored path
        return redirect(stored_path)
    else:
        # Redirect to the index page if no stored path
        return redirect('index')  # Replace 'index' with the actual URL name for your index page

def signUp(request):
    return render(request, "ismartproj/signup.html")


def postsignup(request):

    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')


    try:

        user = authe.create_user_with_email_and_password(email,passw)
    
    except:

        message = "Unable to create account, kindly try again."

        return render(request, "ismartproj/signup.html", {"messages":message})

    uid = user['localId']

    data = {"name":name, "status":"1"}

    database.child("users").child(uid).child("useraccount_details").set(data)

    return render(request, "ismartproj/index.html")

def crops(request):
    try:
        # Verify the Firebase ID token
        id_token = request.session.get('user_id')  # Use the correct session variable name
        if id_token:
            decoded_token = authe.verify_id_token(id_token)
            uid = decoded_token['uid']

            # If the user is authenticated, render the crops page
            return render(request, "ismartproj/crops.html", {"uid": uid})

        # If the user is not authenticated, redirect to the login page
        return redirect('index')  # Replace 'index' with the actual URL name for your login page
    except Exception as e:
        # Print the exception for debugging
        print("Exception in crops:", str(e))
        # If authentication fails, redirect to the login page
        return redirect('index')  # Replace 'index' with the actual URL name for your login page
