# from chatbot import chatbot
from answerer import get_dynamic_answer
import flask_recaptcha
from flask import Flask, render_template, request, session, redirect, flash,url_for
from flask_recaptcha import ReCaptcha
import mysql.connector
from markupsafe import Markup
import psycopg2 
import os

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
app.static_folder = 'static'

# Recaptcha configuration
flask_recaptcha.Markup = Markup
app.config.update(
    RECAPTCHA_ENABLED=True, 
    RECAPTCHA_SITE_KEY="6LfAKEsrAAAAANfmij9uXaudcfcJO7brhQ9Qfeau",
    RECAPTCHA_SECRET_KEY="6LfAKEsrAAAAAPghsnEWUx67X7_d8rfBPgh6k-SC"
)
recaptcha = ReCaptcha(app=app)

# Database connectivity (XAMPP default: root user, no password)
conn = psycopg2.connect(
  host="dpg-d0pvmd8dl3ps73b64sh0-a.oregon-postgres.render.com",
    user="kashish",
    password="CqyEI4gDtw7Td8csg1qZlVw3EnTFl98d",
    dbname="chatbot_00hf",
    port=5432
)
cur = conn.cursor()

# Root route redirects to login page
@app.route("/")
def root():
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/index")
def home():
    if 'id' in session:
        return render_template('index.html')
    return redirect('/login')  # redirect to login if not logged in

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/forgot")
def forgot():
    return render_template('forgot.html')

@app.route("/login_validation", methods=["POST"])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    users = cur.fetchall()

    if users:
        session['id'] = users[0][0]
        flash('You were successfully logged in')
        return redirect('/index')
    else:
        flash('Invalid credentials!')
        return redirect('/login')

@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form.get('name')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    # Insert new user in DB
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    conn.commit()

    # Log the user in after registration
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    myuser = cur.fetchall()
    session['id'] = myuser[0][0]
    flash('You have successfully registered!')
    return redirect('/index')

@app.route("/register_user", methods=["POST"])
def register_user_with_recaptcha():
    if recaptcha.verify():
        flash('New User Added Successfully (ReCaptcha Passed)')
        return redirect('/register')
    else:
        flash('ReCaptcha verification failed')
        return redirect('/register')

@app.route("/suggestion", methods=["POST"])
def suggestion():
    email = request.form.get('uemail')
    message = request.form.get('message')

    cur.execute("INSERT INTO suggestion (email, message) VALUES (%s, %s)", (email, message))
    conn.commit()
    flash('Your suggestion has been successfully sent!')
    return redirect('/index')

@app.route("/logout")
def logout():
    session.pop('id', None)
    flash('You have been logged out')
    return redirect('/login')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_dynamic_answer(userText))

if __name__ == "__main__":
    app.run(debug=True)
