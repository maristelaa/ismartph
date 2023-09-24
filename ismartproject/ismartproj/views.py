from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
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
from firebase_admin import auth, credentials, db

config = {

    "apiKey": "AIzaSyDRo3n2Vau04OzvSoi6kPjSH0hdwDvmXBg",
    "authDomain": "smart-6aa8f.firebaseapp.com",
    "databaseURL": "https://smart-6aa8f-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "smart-6aa8f",
    "storageBucket": "smart-6aa8f.appspot.com",
    "messagingSenderId": "940651613138",
    "appId": "1:940651613138:web:f27e20eb6140e0d7dc160b",
    "serviceAccount":"C:\\Users\\angie\\OneDrive\\Documents\\GitHub\\ismartph\\ismartproject\\firebase\\smart-6aa8f-firebase-adminsdk-xxkfg-e2cb5a121b.json",
}

firebase  = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def logIn(request):
    return render(request, "ismartproj/logIn.html")


def login_required_view(request):
    return HttpResponse("Enter your credentials first.")

def postSign(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('pass')

        print("Starting login process...")  # Added for debugging

        try:
            user = authe.sign_in_with_email_and_password(email, passw)

            # Get the User UID
            user_uid = user['localId']

            # Store the User UID in the session
            request.session['uid'] = str(user_uid)
            
            # Print the session variable for debugging
            print("Firebase UID stored in session:", user_uid)

            # Get the user's UID
            uid = user['localId']
            
            # Retrieve the user's fName from Firebase
            user_data = database.child("users").child(uid).child("useraccount_details").get().val()
            fname = user_data.get("fname")
            lname = user_data.get("lname")
            
            
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
        

            # Get the previously stored 'current_path' (if it exists)
            current_path = request.session.get('current_path')

            if current_path:
                # Redirect to the stored path
                return redirect(current_path)
            else:
                # If there's no stored path, redirect to the home page
                return render(request, 'ismartproj/home.html', {'e':email, 'fname': fname, 'lname':lname})
        except Exception as e:
            # Print the exception for debugging
            print("Exception in postSign:", str(e))
            message = "Invalid Email or Password"
            return render(request, "ismartproj/logIn.html", {"messg": message})
    else:
        # Handle GET request (render the login page)
        return render(request, "ismartproj/logIn.html")


def logout_required_view(request):
    response = HttpResponse("Kindly logout your account first.")
    response


def signOut(request):
    try:
        # Clear the Firebase UID session variable
        del request.session['uid']

        # Sign out the user from Firebase authentication
        auth.logout(request)

        # Redirect to the index page or any other appropriate page after logout
        return redirect('index')  # Replace 'index' with the actual URL name for your login page
    except Exception as e:
        # Print the exception for debugging
        print("Exception in signOut:", str(e))
        return HttpResponse("An error occurred during logout.")

#

def signOut(request):
    try:
        # Get the Firebase UID from the session
        uid = request.session.get('uid')

        if uid:
            # Sign out the user from Firebase authentication
            authe.logout(request)

            # Clear the Firebase UID session variable
            del request.session['uid']

            # Display a success message
            print("User {uid} has successfully logged out.")
            return render(request, "index.html")
        else:
            # If the UID is not found in the session, it means the user is not authenticated
            # Redirect to the index page or any other appropriate page
            return redirect('index')  # Replace 'index' with the actual URL name for your login page
    except Exception as e:
        # Print the exception for debugging
        print("Exception in signOut:", str(e))
        return HttpResponse("An error occurred during logout.")


def signUp(request):
    return render(request, "ismartproj/register_user.html")


def postsignup(request):

    firstname = request.POST.get('fname')
    lastname = request.POST.get('lname')
    middlename = request.POST.get('mname')
    suffixname = request.POST.get('sname')

    codeModel = request.POST.get('iot_code')

    email = request.POST.get('email')
    passw = request.POST.get('pass')


    try:

        user = authe.create_user_with_email_and_password(email,passw)
    
    except:

        message = "Unable to create account, kindly try again."

        return render(request, "ismartproj/register_user.html", {"messages":message})

    uid = user['localId']

    data1 = {
            "fname":firstname, 
            "mname":middlename, 
            "lname":lastname, 
            "sname":suffixname,
            "status":"1"
        }
    
    data2 = {"iot_code":codeModel}

    database.child("users").child(uid).child("useraccount_details").set(data1)
    database.child("IOT").child(uid).child("IoT_Code").set(data2)

    return render(request, "ismartproj/logIn.html")



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
    try:
        # Verify the Firebase UID in the session
        uid = request.session.get('uid')
        if uid:
            # If the user is authenticated, render the crops page
            return render(request, "ismartproj/home.html", {"uid": uid})

        # If the user is not authenticated, redirect to the login page
        return redirect('index')  # Replace 'index' with the actual URL name for your login page
    except Exception as e:
        # Print the exception for debugging
        print("Exception in crops:", str(e))
        # If authentication fails, redirect to the login page
        return redirect('index')  # Replace 'index' with the actual URL name for your login page




def mycrop(request):
    return render(request, "ismartproj/mycrop.html")

def crops(request):
    return render(request, "ismartproj/crops.html")
#try



#def crops(request):
    try:
        # Retrieve the Firebase UID and ID token from the session
        uid = request.session.get('uid')
        id_token = request.session.get('id_token')

        # Check if both UID and ID token are available
        if uid and id_token:
            try:
                # Verify the ID token using Firebase Admin SDK
                decoded_token = authe.verify_id_token(id_token)
                
                # Check if the token is valid and the user's email is verified
                if decoded_token and decoded_token['email_verified']:
                    # User is authenticated, render the crops page
                    return render(request, "ismartproj/crops.html", {"uid": uid})
                else:
                    # User is not authenticated or email is not verified, redirect to the login page
                    return redirect('logIn')  # Replace 'index' with the actual URL name for your login page
            except Exception as e:
                # Token verification failed, redirect to the login page
                return redirect('logIn')  # Replace 'index' with the actual URL name for your login page
        else:
            # If the UID or ID token is not found in the session, it means the user is not authenticated
            # Redirect to the login page
            message = "token is not found in the session"
            return redirect('logIn', {"messg": message + str(e)}) # Replace 'index' with the actual URL name for your login page
    except Exception as e:
        # Print the exception for debugging
        print("Exception in crops:", str(e))
        # If any other exception occurs, redirect to the login page
        return redirect('logIn')  # Replace 'index' with the actual URL name for your login page


#start of the progress of algo
# Get today's date in the format "Sep-21-2023"
import datetime
import csv

# Function to save data to CSV file
def save_data_to_csv(data, filename='data.csv'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_to_write = [timestamp] + data  # Add timestamp to the data

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_to_write)


def fetch_data(request):
    today_date = datetime.datetime.now().strftime("%b-%d-%Y")

    # Fetch the temperature data for today
    temp_data = database.child("IOT").child("15004526").child("S1").child("DATA").child("TEMP").child(today_date).get().val()
    sml_data = database.child("IOT").child("15004526").child("S1").child("DATA").child("SML").child(today_date).get().val()
    humid_data = database.child("IOT").child("15004526").child("S1").child("DATA").child("HUMIDITY").child(today_date).get().val()


    most_recent_temp_data = None
    most_recent_sml_data = None
    most_recent_hum_data = None


    # Process temperature data
    if temp_data:
        most_recent_temp_time = None
        most_recent_temp = None

        for time, temp in temp_data.items():
            if isinstance(temp, (int, float)) and isinstance(time, str) and ':' in time:
                time_obj = datetime.datetime.strptime(time, "%H:%M")

                if most_recent_temp_time is None or time_obj > most_recent_temp_time:
                    most_recent_temp_time = time_obj
                    most_recent_temp = temp

        if most_recent_temp_time is not None:
            most_recent_temp_time_str = most_recent_temp_time.strftime("%H:%M")
            most_recent_temp_data = {
                "time": most_recent_temp_time_str,
                "temperature": most_recent_temp
            }

    # Process SML data
    if sml_data:
        most_recent_sml_time = None
        most_recent_sml = None

        for time, sml in sml_data.items():
            if isinstance(sml, (int, float)) and isinstance(time, str) and ':' in time:
                time_obj = datetime.datetime.strptime(time, "%H:%M")

                if most_recent_sml_time is None or time_obj > most_recent_sml_time:
                    most_recent_sml_time = time_obj
                    most_recent_sml = sml

        if most_recent_sml_time is not None:
            most_recent_sml_time_str = most_recent_sml_time.strftime("%H:%M")
            most_recent_sml_data = {
                "time": most_recent_sml_time_str,
                "sml_value": most_recent_sml
            }
            
            
    # Process SML data
    if humid_data:
        most_recent_hum_time = None
        most_recent_hum = None

        for time, hum in humid_data.items():
            if isinstance(sml, (int, float)) and isinstance(time, str) and ':' in time:
                time_obj = datetime.datetime.strptime(time, "%H:%M")

                if most_recent_hum_time is None or time_obj > most_recent_hum_time:
                    most_recent_hum_time = time_obj
                    most_recent_hum = hum

        if most_recent_hum_time is not None:
            most_recent_hum_time_str = most_recent_hum_time.strftime("%H:%M")
            most_recent_hum_data = {
                "time": most_recent_hum_time_str,
                "humid_value": most_recent_hum
            }
            
    # Save the fetched data to CSV
    if most_recent_temp_data:
        save_data_to_csv([most_recent_temp_data["time"], most_recent_temp_data["temperature"]], 'temperature.csv')
    if most_recent_sml_data:
        save_data_to_csv([most_recent_sml_data["time"], most_recent_sml_data["sml_value"]], 'sml.csv')
    if most_recent_hum_data:
        save_data_to_csv([most_recent_hum_data["time"], most_recent_hum_data["humid_value"]], 'humidity.csv')

    return render(request, 'ismartproj/fetch_data.html', {
        'most_recent_temp_data': most_recent_temp_data,
        'most_recent_sml_data': most_recent_sml_data,
        'most_recent_hum_data': most_recent_hum_data,
    }
)
