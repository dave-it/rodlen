# app.py

from flask import Flask, render_template, request, current_app, jsonify
from timer import start_timer, stop_timer
from athletes import add_athlete, get_all_athletes, init_db, get_athlete_data, get_db
import csv
import codecs  # Fügen Sie diese Zeile hinzu

app = Flask(__name__)

# Initialisiere die Datenbank beim Start der Anwendung
with app.app_context():
    init_db()

@app.route('/')
def index():
    athletes = get_all_athletes()
    return render_template('index.html', athletes=athletes)

@app.route('/start', methods=['POST'])
def start():
    global timer_running
    print("IN START?")
    timer_running = True

    start_number = int(request.form.get('start_number'))
    athlete_data = get_athlete_data(start_number)

    if athlete_data:
        duration_minutes = 5  # Set the desired duration in minutes
        duration_seconds = duration_minutes * 60
        print("DATA")
        start_timer(duration_seconds, athlete_data)
        print("SUCCESS??")
        # Sendet eine JSON-Antwort mit einer Meldung für das Popup
        return jsonify({'status': 'success', 'message': 'Timer started successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'Athlete not found or data incomplete.'})

@app.route('/stop', methods=['POST'])
def stop():
    global timer_running
    stop_timer()
    return jsonify({'status': 'success', 'message': 'Timer stopped successfully!'})


@app.route('/get_runtime', methods=['POST'])
def get_runtime():
    start_number = request.form.get('start_number')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Rufe die Laufzeit für den angegebenen Athleten ab
    cursor.execute('SELECT runtime FROM athletes WHERE start_number = ?', (start_number,))
    result = cursor.fetchone()
    
    conn.close()

    if result:
        return jsonify({'runtime': result[0]})
    else:
        return jsonify({'runtime': 0})


@app.route('/import_csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    if file and file.filename.endswith('.csv'):
        try:
            # Änderungen hier: Die Datei mit codecs.iterdecode öffnen
            decoded_file = codecs.iterdecode(file, 'utf-8')
            save_csv_to_database(decoded_file)
            return jsonify({'status': 'success', 'message': 'CSV data imported successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error importing CSV data: {str(e)}'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid file format. Please upload a CSV file'})


def save_csv_to_database(csv_file):
    conn = get_db()
    cursor = conn.cursor()

    # Annahme: CSV-Datei hat Spaltenüberschriften in der ersten Zeile
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        cursor.execute('''
            INSERT INTO athletes (first_name, last_name, nation, birthdate, start_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['First Name'], row['Last Name'], row['Nation'], row['Birthdate'], row['Start Number']))

    conn.commit()
    conn.close()

    return True

@app.route('/top_drivers', methods=['GET'])
def top_drivers():
    conn = get_db()
    cursor = conn.cursor()

    # Annahme: Die Tabelle heißt 'athletes'
    # Den globalen Offset-Wert aus der Datenbank abrufen
    cursor.execute('SELECT offset FROM global_settings WHERE id = 1')
    global_offset = cursor.fetchone()[0]

    # SQL-Abfrage mit dem globalen OFFSET-Wert
    cursor.execute('SELECT * FROM athletes ORDER BY start_number LIMIT 10 OFFSET ?', (global_offset,))
    drivers = cursor.fetchall()

    conn.close()

    flag_path = 'C:\\Users\\David\\Downloads\\'

    # Konvertieren Sie die Daten in ein JSON-Format
    drivers_json = [
        {
            'id': driver[0],
            'first_name': driver[1],
            'last_name': driver[2],
            'nation': driver[3],
            'birthdate': driver[4],
            'start_number': driver[5],
            'runtime': driver[6],
            'split1': driver[7],
            'split2': driver[8],
            'split3': driver[9],
            'split4': driver[10],
            'split5': driver[11],
            'name': driver[2].upper() + ' '  + driver [1],
            'flag_path': flag_path + driver[3] + '.png'
        } for driver in drivers
    ]
    while len(drivers_json) < 10:
        empty_driver = {
            'id': '',
            'first_name': '',
            'last_name': '',
            'nation': '',
            'birthdate': '',
            'start_number': '',
            'runtime': '',
            'split1': '',
            'split2': '',
            'split3': '',
            'split4': '',
            'split5': '',
            'name': '',
            'flag_path': flag_path + 'EMP.png'
        }
        drivers_json.append(empty_driver)

    return jsonify({'top_drivers': drivers_json})

@app.route('/update_global_offset/<int:new_offset>', methods=['POST'])
def update_global_offset(new_offset):
    conn = get_db()
    cursor = conn.cursor()

    # Annahme: Die Tabelle heißt 'global_settings'
    # Den globalen Offset-Wert in der Datenbank aktualisieren
    cursor.execute('UPDATE global_settings SET offset = ? WHERE id = 1', (new_offset,))
    conn.commit()

    conn.close()

    return jsonify({'status': 'success', 'message': 'Global offset updated successfully'})


if __name__ == "__main__":
    app.run(debug=True)
