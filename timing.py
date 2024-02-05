import time
import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)

DATABASE = 'athletes.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def update_timer_file(file_path, minutes, seconds):
    with open(file_path, 'w') as file:
        file.write(f"{minutes} minutes and {seconds} seconds")

def timer(duration):
    start_time = time.time()
    while True:
        if not timer_running:
            break

        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        update_timer_file("timer.txt", minutes, seconds)
        time.sleep(1)

        if elapsed_time >= duration:
            break

    print("Timer completed!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_timer():
    global timer_running
    timer_running = True

    duration_minutes = 5  # Set the desired duration in minutes
    duration_seconds = duration_minutes * 60
    timer(duration_seconds)

    return "Timer started!"

@app.route('/stop', methods=['POST'])
def stop_timer():
    global timer_running
    timer_running = False
    return "Timer stopped!"

@app.route('/add_athlete', methods=['POST'])
def add_athlete():
    # Erhalte die Daten aus dem Formular
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    nation = request.form.get('nation')
    birthdate = request.form.get('birthdate')
    start_number = request.form.get('start_number')

    # Füge den Athleten zur Datenbank hinzu
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO athletes (first_name, last_name, nation, birthdate, start_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, nation, birthdate, start_number))
    db.commit()

    return f"Athlete {first_name} {last_name} added successfully!"

if __name__ == "__main__":
    app.run(debug=True)