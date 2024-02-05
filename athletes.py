import sqlite3
from flask import current_app, g, request

DATABASE = 'athletes.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with current_app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS athletes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            nation TEXT NOT NULL,
            birthdate TEXT NOT NULL,
            start_number INTEGER NOT NULL,
            runtime INTEGER DEFAULT 0,
            split1 INTEGER DEFAULT 0,
            split2 INTEGER DEFAULT 0,
            split3 INTEGER DEFAULT 0,
            split4 INTEGER DEFAULT 0,
            split5 INTEGER DEFAULT 0
            )
        ''')    

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_settings (
            id INTEGER PRIMARY KEY,
            offset INTEGER
        )
        ''')    

        cursor.execute('''
        INSERT OR IGNORE INTO global_settings (offset) VALUES (0);
        ''')    
        db.commit()

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

def get_all_athletes():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM athletes')
    athletes = cursor.fetchall()
    print(athletes)
    return athletes

def get_athlete_data(start_number):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            SELECT * FROM athletes
            WHERE start_number = ?
        ''', (start_number,))
        athlete = cursor.fetchone()

    if athlete:
        athlete_data = {
            'first_name': athlete['first_name'],
            'last_name': athlete['last_name'],
            'nation': athlete['nation'],
            'birthdate': athlete['birthdate'],
            'start_number': athlete['start_number']
            # Weitere Attribute hier hinzufügen
        }
        return athlete_data
    else:
        return None