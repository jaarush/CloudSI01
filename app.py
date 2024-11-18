from flask import Flask, render_template, request, redirect, url_for
import pyrebase
import requests
import datetime

app = Flask(__name__)

# Firebase configuration
firebase_config = {
    "apiKey": "YOUR_FIREBASE_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# OpenWeatherMap API configuration
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    # Fetch all weather data entries
    weather_entries = db.child("weather").get().val()
    return render_template("index.html", weather_entries=weather_entries)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get("city")
    response = requests.get(WEATHER_URL, params={
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    })

    if response.status_code == 200:
        weather_data = response.json()
        entry = {
            "city": city,
            "temperature": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Save weather data in Firebase
        db.child("weather").push(entry)
    return redirect(url_for("index"))

@app.route('/delete/<string:entry_id>')
def delete_entry(entry_id):
    # Delete an entry from Firebase
    db.child("weather").child(entry_id).remove()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
