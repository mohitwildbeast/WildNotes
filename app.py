#Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'secretkey'

#Databse connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Hello@123'
app.config['MYSQL_DB'] = 'wildnotes'

#Initilaize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('index.html')

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
			return redirect(url_for('home'))
		else:
			msg = 'Invalid Credentials. Please Try Again!'
	return render_template('login.html', msg=msg)

@app.route('/logout/')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   return redirect(url_for('login'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'name' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Name must contain only characters and numbers!'
        elif not name or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (email, password, name))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/home/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/profile/')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/profile/deleteProfile/', methods=['GET', 'POST'])
def deleteProfile():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('DELETE FROM users WHERE id = %s', [session['id']])
		mysql.connection.commit()
		msg = 'Account successfully deleted.'
		return render_template('register.html', msg=msg)

@app.route('/profile/editProfile/', methods=['GET', 'POST'])
def editProfileView():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
		account = cursor.fetchone()
	return render_template('editProfileView.html', account=account)

@app.route('/profile/', methods=['GET', 'POST'])
def editProfile():
	if 'loggedin' in session:
		name = request.form['name']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('UPDATE users SET email=%s, password = %s, name = %s WHERE id = %s', [email, password, name, session['id']])
		mysql.connection.commit()
		return redirect(url_for('profile'))

@app.route('/notes/addnote/', methods=['GET','POST'])
def addNoteView():
	return render_template('addNoteView.html')

@app.route('/home/', methods=['GET', 'POST'])
def addNote():
	if 'loggedin' in session:
		note = request.form['note']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO notes VALUES (NULL, %s, %s)', (note, session['id']))
		mysql.connection.commit()
		return render_template('home.html')

@app.route('/notes/viewnotes/', methods=['GET','POST'])
def viewNotes():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM notes WHERE userid = %s', [session['id']])
		data = cursor.fetchall()
	return render_template('viewNotes.html', data=data)

@app.route('/notes/deletenote/', methods=['GET','POST'])
def deleteNote():
	if 'loggedin' in session:
		noteid = request.form['noteid']
		print(noteid)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('DELETE FROM notes WHERE noteid = %s', [noteid])
		mysql.connection.commit()
		return redirect(url_for('viewNotes'))

@app.route('/notes/editNoteView/', methods=['GET','POST'])
def editNoteView():
	if 'loggedin' in session:
		noteid = request.form['noteid']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM notes WHERE noteid = %s', [noteid])
		note = cursor.fetchone()
		print(note)
	return render_template('editNoteView.html', note = note)

@app.route('/notes/editnote/', methods=['GET','POST'])
def editNote():
	if 'loggedin' in session:
		noteid = request.form['noteid']
		note = request.form['note']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('UPDATE notes SET content = %s WHERE noteid = %s',[note,noteid])
		mysql.connection.commit()
		return redirect(url_for('viewNotes'))

if __name__ == '__main__':
    app.run(debug=True)