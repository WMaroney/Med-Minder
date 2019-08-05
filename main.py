# Imports
from flask import render_template, flash, redirect, url_for, request, Flask, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, DateTimeField, TextField, PasswordField, validators, SubmitField, TextAreaField, RadioField, IntegerField, FloatField, FileField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import sys
import pymysql #used to connect SQL DB to python and run queries
import sqlite3
import getpass
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
import uuid
from werkzeug.utils import secure_filename
import os
import datetime
import re

db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
c = db.cursor()

## FLASK FORMS subclassed from FlaskForm


class LoginForm(FlaskForm):
	username = TextField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
	username = TextField('Username', validators=[DataRequired()])
	#Add built in Validator
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPass', message='Passwords must match')])
	confirmPass = PasswordField('Repeat Password', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

class ConfirmMedicationAdd(FlaskForm):
	submit = SubmitField('Confirm')

# Add Rx Manual Form
class AddManual(FlaskForm):
	medication = StringField('Medication', validators=[DataRequired()])
	dosage = IntegerField('Dosage', validators=[DataRequired()])
	freq = StringField('Frequency', validators=[DataRequired()])
	refills = IntegerField('Refills', validators=[DataRequired()])
	dateFill = DateTimeField('Date Filled', validators=[DataRequired()])
	doc = StringField('Physician', validators=[DataRequired()])
	pharm = StringField('Pharmacy', validators=[DataRequired()])
	submit =  SubmitField('Submit: ')

class AddScan(FlaskForm):
	# Initiate OCR to get text file
	submit =  SubmitField('Add Prescription via Camera')

# Remove Rx Form
class Remove(FlaskForm):
	medication = StringField('Medication', validators=[DataRequired()])
	submit =  SubmitField('Remove Prescription')

## User class

class User(UserMixin):
	def __init__(self, ident, username, name, email, setup, password, role):
		self.id = username.replace("'", "")
		# hash the password and output it to stderr
		self.pass_hash = password
		self.role = role
		self.name = name
		self.email = email
		self.profileSetup = int(setup)
		self.ident = ident

class Medication():
	def __init__(self, id, addedDate, dosage, freq, refill):
		self.id = id
		self.addedDate = addedDate
		self.dosage = dosage
		self.freq = frequency
		self.refill = refills


## Creating the Flask app object and login manager

app = Flask(__name__)

skey = os.urandom(12)
app.config['SECRET_KEY'] = skey
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
images_folder = 'documents/rx_images/'
translation_folder = 'documents/text_translations/'
allowed_extensions = set(['txt', 'jpg'])

# Code for allowed file extensions

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Code to load users and meds as functions to load later

def load_users():
	c.execute("SELECT * from users")
	users = c.fetchall()
	for user in users:
		user_db["" + str(user[2])] = User(user[0],"'" + user[2] + "'",user[1],user[2],user[3],user[4],user[5],user[6],user[7],user[8],user[9],user[10], 'user')
		print(user_db.get(str(user[2].replace("'", ""))).id + ": Created as User")
	
def load_meds():
	c.execute("SELECT * from usermeds")
	meds = c.fetchall()
	for med in meds:
		med_db[str(app[0])] = Medication(med[0],med[1],med[2],med[3],med[4],med[5],med[6])
		print(str(med_db.get(str(med[0])).id) + ": Created as Medication")

# Init User and Medication Databases

user_db = {}
med_db = {}

load_users()
load_meds()

#Dictionary of invites sent to users
invite_db = {}

#Dictionary of verifies sent to users
verify_db = {}

def checkUUID(ID, selectList):
	if selectList == "verify":
		return verify_db.get(ID)
	elif selectList == "invite":
		return invite_db.get(ID)
	else:
		return None
	
def verifyEmail(email, password, role):
	fromaddr = "medmindercsc400@gmail.om"
	toaddr = email
	
	#Generate hex UUID which is unique and save this to the invite_db
	x = uuid.uuid1()
	verify_db[str(x)] = [email, password, role]
	
	body = "Please click the link below to verify your account! <br><a href='http://127.0.0.1:5000/verify/" + str(x) + "'>Link</a>"
	msg = MIMEText(body, 'html')
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Med-Minder Verify Email"
	server = smtplib.SMTP('smtp-relay.gmail.com')
	server.starttls()
	server.login("medmindercsc400@gmail.com", "Atmose@123")
	text = msg.as_string()
	server.sendmail(fromaddr,[toaddr],text)
	server.quit()
	
def profileIsSetup():
	if current_user.profileSetup == 1:
		return True
	else:
		return False
	


# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.
@login_manager.user_loader
def load_user(id):
	return user_db.get(id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
	c = db.cursor()
	c.execute('SELECT * from usermeds')
	l = c.fetchall()
	db.close()
	return render_tamplate ('index.html', data=l)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	# display the login form
	form = LoginForm()
	if form.validate_on_submit():
		user = user_db[form.username.data]
		# validate user
		valid_password = check_password_hash(user.pass_hash, form.password.data)
		if user is None or not valid_password:
			print('Invalid username or password', file=sys.stderr)
			redirect(url_for('index'))
		else:
			print(user)
			login_user(user)
			print(user.is_authenticated)
			flash('Login Successful', category='success')
			return redirect(url_for('index'))

	return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	# display the login form
	form = SignupForm()
	if form.validate_on_submit():
		user = form.username.data
		exists = user_db.get(user)
		# validate user
		if exists is None:
			user_pass = generate_password_hash(form.password.data)
			verifyEmail(user, user_pass, "student")
			flash('Please check your email to verify your account', category='info')
			return redirect(url_for('index'))
		else:
			flash('Invalid User Name or Password', category='error')
			return redirect(url_for('index'))

	return render_template('signUP.html', title='Sign Up', form=form)



@app.route('/addrxman', methods=['GET', 'POST'])
def addrxman():
	form = AddManual()
	if form.validate_on_submit():
		db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
		c = db.cursor()
		sql = 'INSERT INTO usermeds(med_name, med_dose, num_refills, med_freq) VALUES'\
		"(%s, %s, %s, %s)"
		c.execute (sql, (usermeds, str(med_name), int(med_dose), int(num_refills), int(med_freq)))
		db.commit()
		db.close()
		return (redirect('/view'))
	return render_template('index.html', form_add=form)


@app.route('/remove',methods=['GET', 'POST'])
def removerx():
	form = Remove()
	if form.validate_on_submit():
		db = pymysql.connect(host='35.229.79.169', user='root', password='password', db='med_minder')
		c = db.cursor()
		sql = "DELETE FROM usermeds WHERE name = '"+med_name+"'"
		c.execute (sql)
		db.commit()
		db.close()
		return (redirect('/view'))
		return render_template('index.html', form_add=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/about')
def about():
	return render_template('about.html', title='About')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
