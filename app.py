from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

# Define the database file path
DATABASE_FILE = 'users.db'

# Create users table if not exists
def create_users_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert a new user into the database
def insert_user(email, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashlib.sha256(password.encode()).hexdigest()))
    conn.commit()
    conn.close()

# Check if the email and password are valid
def authenticate_user(email, password):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, hashlib.sha256(password.encode()).hexdigest()))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate_user(email, password):
            return redirect(url_for('end'))
        else:
            return 'Invalid email or password'
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        insert_user(email, password)
        return redirect(url_for('login'))  # Redirect to login page after successful signup
    return render_template('signup.html')

@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)
