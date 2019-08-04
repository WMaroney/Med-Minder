# Imports
from flask import render_template, flash, redirect, url_for, request, Flask, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, TextField, PasswordField, validators, SubmitField, TextAreaField, RadioField, IntegerField, DateTimeField, FileField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
import sys
import pymysql 
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

db = pymysql.connect(host='35.237.157.161', user='root', password='password', db='med-minder')
c = db.cursor()

## FLASK FORMS subclassed from FlaskForm##


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
class Add_Manual(FlaskForm):
	medication = StringField('Medication', validators=[DataRequired()])
	dosage = IntegerField('Dosage', validators=[DataRequired()])
	freq = StringField('Frequency', validators=[DataRequired()])
	refills = IntegerField('Refills', validators=[DataRequired()])
	dateFill = DateTimeField('Date Filled', validators=[DataRequired()])
	doc = StringField('Physician', validators=[DataRequired()])
	pharm = StringField('Pharmacy', validators=[DataRequired()])
	submit =  SubmitField('Submit: ')
	
class Add_Scan(FlaskForm):
	# Initiate OCR to get text file
	submit =  SubmitField('Add Prescription via Camera')

# Remove Rx Form	
class Remove(FlaskForm):
	medication = StringField('Medication', validators=[DataRequired()])
	submit =  SubmitField('Remove Prescription')
	
	
	
	
## User class, subclassed from UserMixin for convenience.  UserMixin
## provides attributes to manage user (e.g. authenticated). 	
	
	
class User(UserMixin):
	def __init__(self, ident, username, setup, password):
		self.id = username.replace("'", "")
		# hash the password and output it to stderr
		self.pass_hash = password
		self.ident = ident
		self.profileSetup = int(setup)
		
		
class Medication():
	def __init__(self, id, addedDate, dosage, freq, refill):
		self.id = id
		self.addedDate = addedDate
		self.dosage = dosage
		self.freq = frequency
		self.refill = refills


## Creating the Flask app object and login manager
	
app = Flask(__name__)

# app.config['SECRET_KEY'] = 'mf0439mf028nf4024wevwve'. CHECK THIS OUT FROM GCP
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
images_folder = 'documents/rx_images/'
translation_folder = 'documents/text_translations/'
allowed_extensions = set(['txt', 'jpg'])



# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in allowed_extensions


# Init User and Medication Databases
	
user_db = {}
med_db = {}	

# Verification email on account creation	
	
def verifyEmail(email, password, role):
	fromaddr = "medmindercsc400@gmail.com"
	toaddr = email
	
	#Generate hex UUID which is unique and save this to the invite_db
	x = uuid.uuid1()
	verify_db[str(x)] = [email, password, role]
	
	body = "Please click the link below to verify your account! <br><a href='http://127.0.0.1:5000/verify/" + str(x) + "'>Link</a>"
	msg = MIMEText(body, 'html')
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Med_Minder Verify Email"
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login("medmindercsc400@gmail.com", "Atmose@123")
	text = msg.as_string()
	server.sendmail(fromaddr,[toaddr],text)
	server.quit()
	
#Check if current user has created their profile!
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


def viewrx():
	db=pymysql.connect(host='35.237.157.161', user='root', password='123', db='med_minder')
	c = db.cursor()
	c.execute('SELECT * from medications')
	l = c.fetchall()
	db.close()
	return render_tamplate ('index.html', data=l)

	
	
@app.route('/add_manual', methods=['GET', 'POST'])
def addrx():
	form = Add()
	if form.validate_on_submit():
		city = form.city.data
		population = form.pop.data
		db=pymysql.connect(host='35.237.157.161', user='root', password='123', db='med_minder')
		c = db.cursor()
		sql = 'INSERT INTO medicaton(name, dosage, refill, frequency) VALUES'\
		"(%s, %s, %s, %s)"
		c.execute (sql, (medication, str(name), int(dosage), int(refill), int(frequency)))
		db.commit()
		db.close()
		return (redirect('/view'))
	return render_template('index.html', form_add=form)	


@app.route('/remove',methods=['GET', 'POST'])
def removerx():
	form = Remove()
	if form.validate_on_submit():
		city = form.city.data
		db=pymysql.connect(host='35.237.157.161', user='root', password='123', db='med_minder')
		c = db.cursor()
		sql = "DELETE FROM medication WHERE name = '"+medication+"'"
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
