from flask import Flask, render_template, request, redirect, url_for
import pyrebase

app = Flask(__name__)

# Firebase configuration
firebase_config = {
    "apiKey": "YOUR_API_KEY",
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

@app.route('/')
def index():
    # Fetch all to-do items
    todos = db.child("todos").get().val()
    return render_template("index.html", todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    # Add a new to-do item
    todo_item = request.form.get("todo")
    db.child("todos").push({"task": todo_item})
    return redirect(url_for("index"))

@app.route('/delete/<string:todo_id>')
def delete_todo(todo_id):
    # Delete a to-do item
    db.child("todos").child(todo_id).remove()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
