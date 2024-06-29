from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
import os
# Bearerトークン envから
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

@app.route('/')
def home():
    is_logged_in = session.get('logged_in', False)
    if not is_logged_in:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM problems')
    problems = cur.fetchall()
    return render_template('index.html', problems=problems)

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == os.environ.get('SITE_PASSWORD'):
            flash('Logged in successfully.')
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')        
    return render_template('login.html')

@app.route('/add_problem', methods=['POST'])
def add_problem():
    name = request.form['title']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO problems (title) VALUES (%s)', (name,))
    mysql.connection.commit()
    return redirect(url_for('home'))


mapping = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"

def encode_text(text):
    encoded_text = ""
    for c in text:
        encoded_text += chr(mapping.index(c) + 33)
    return 'S' + encoded_text

@app.route('/problem_detail/<int:problem_id>', methods=['GET', 'POST'])
def problem_detail(problem_id):
    is_logged_in = session.get('logged_in', False)
    if not is_logged_in:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT title FROM problems WHERE id = %s', (problem_id,))
    problem_title = cur.fetchone()['title']

    if request.method == 'POST':
        user_input = request.form['user_input']
        url = "https://boundvariable.space/communicate"
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'text/plain'
        }
        data = f"solve {problem_title} {user_input}"
        data = encode_text(data)
        
        response = requests.post(url, headers=headers, data=data)
        # 提出と結果を保存
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO submissions (problem_id, user_input, result) VALUES (%s, %s, %s)",
                    (problem_id, data, response.text))
        mysql.connection.commit()
        return redirect(url_for('problem_detail', problem_id=problem_id))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM submissions WHERE problem_id = %s ORDER BY id DESC', (problem_id,))
    submissions = cur.fetchall()
    cur = mysql.connection.cursor()
    
    return render_template('problem_detail.html', problem_title=problem_title, submissions=submissions)



