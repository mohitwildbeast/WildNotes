#Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

#Databse connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hello@123'
app.config['MYSQL_DB'] = 'wildnotes'

#Initilaize MySQL
mysql = MySQL(app)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	msg = ''
	if(request.method == 'POST' and 'email' in request.form and 'password' in request.form):
		email = request.form['email']
		password = request.form['password']
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email,password))
		user = cursor.fetchone()

		if(user):
			session['loggedin'] = True
			session['id'] = user['id']
			session['email'] = user['email']
			return 'Logged In Successfully!'
		else:
			msg = 'Invalid Credentials. Please Try Again!'
	return render_template('login.html', msg=msg)

@app.route('/logout/')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   return redirect(url_for('login'))

