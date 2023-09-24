from ismartproject.celery import shared_task
from ismartproj.views import save_data_to_csv
import datetime
import datetime
import firebase_admin
from firebase_admin import credentials
import pyrebase
import csv


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


# tasks.py

@shared_task
def fetch_and_save_data_periodically():
    today_date = datetime.datetime.now().strftime("%b-%d-%Y")

    # Fetch the temperature data for today from Firebase (similar to your existing code)
    temp_data = database.child("IOT").child("15004526").child("S1").child("DATA").child("TEMP").child(today_date).get().val()
    sml_data = database.child("IOT").child("15004526").child("S1").child("DATA").child("SML").child(today_date).get().val()
    humid_data = database.child("IOT").child("15004526").child("S1").child("DATA").child("HUMIDITY").child(today_date).get().val()

    # Process and save the temperature data to CSV
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

            # Save the fetched temperature data to a CSV file
            save_data_to_csv([most_recent_temp_time_str, most_recent_temp], 'temperature.csv')

    # Process and save the SML data to CSV (similar logic as temperature)
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

            # Save the fetched SML data to a CSV file
            save_data_to_csv([most_recent_sml_time_str, most_recent_sml], 'sml.csv')

    # Process and save the humidity data to CSV (similar logic as temperature)
    if humid_data:
        most_recent_hum_time = None
        most_recent_hum = None

        for time, hum in humid_data.items():
            if isinstance(hum, (int, float)) and isinstance(time, str) and ':' in time:
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

            # Save the fetched humidity data to a CSV file
            save_data_to_csv([most_recent_hum_time_str, most_recent_hum], 'humidity.csv')
