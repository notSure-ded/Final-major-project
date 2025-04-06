from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
import sqlite3
from chatbot import get_bot_response  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uwu'
socketio = SocketIO(app)

def get_db_connection():
    conn = sqlite3.connect('university.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM students WHERE email = ? AND password = ?',
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session['student_id'] = user['student_id']
            flash("Login successful", "success")
            return redirect(url_for('chat'))
        else:
            flash("Invalid email or password. Try again, brainiac.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db_connection()
        existing = conn.execute(
            'SELECT * FROM students WHERE roll_no = ? OR email = ?',
            (roll_no, email)
        ).fetchone()

        if existing:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

        conn.execute(
            'INSERT INTO students (name, roll_no, email, phone, password) VALUES (?, ?, ?, ?, ?)',
            (name, roll_no, email, phone, password)
        )
        conn.commit()
        conn.close()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM students WHERE student_id = ?', (session['student_id'],)).fetchone()
    conn.close()

    return render_template('index.html', name=user['name'], student_id=user['student_id'], email=user['email'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@socketio.on('user_message')
def handle_message(data):
    msg = data['message']
    student_id = session.get("student_id")
    reply = get_bot_response(msg, student_id) 
    emit('bot_reply', {'message': reply})

if __name__ == '__main__':
    socketio.run(app, debug=True)
