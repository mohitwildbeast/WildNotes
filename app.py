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
	return render_template('login.html', msg = '')
