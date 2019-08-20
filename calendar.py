from __future__ import print_function
import httplib2
import os
import pickle
from apiclient import discovery
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
		flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=SCOPES)
credentials = flow.run_console()
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Med-Minder'
pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()

def get_credentials():
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
				Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
				os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

		store = oauth2client.file.Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
				flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
				flow.user_agent = APPLICATION_NAME
				if flags:
						credentials = tools.run_flow(flow, store, flags)
				else: # Needed only for compatibility with Python 2.6
						credentials = tools.run(flow, store)
				print('Storing credentials to ' + credential_path)
		return credentials

def create_event():
		"""Shows basic usage of the Google Calendar API.

		Creates a Google Calendar API service object and outputs a list of the next
		10 events on the user's calendar.
		"""
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('calendar', 'v3', http=http)

		# Refer to the Python quickstart on how to setup the environment:
		# https://developers.google.com/google-apps/calendar/quickstart/python
		# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
		# stored credentials.

		event = {
			'summary': 'Google I/O 2015',
			'location': '800 Howard St., San Francisco, CA 94103',
			'description': 'A chance to hear more about Google\'s developer products.',
			'start': {
				'dateTime': '2016-09-28T09:00:00-07:00',
				'timeZone': 'America/Los_Angeles',
			},
			'end': {
				'dateTime': '2016-09-28T17:00:00-07:00',
				'timeZone': 'America/Los_Angeles',
			},
			'recurrence': [
				'RRULE:FREQ=DAILY;COUNT=2'
			],
			'attendees': [
				{'email': 'lpage@example.com'},
				{'email': 'sbrin@example.com'},
			],
			'reminders': {
				'useDefault': False,
				'overrides': [
					{'method': 'email', 'minutes': 24 * 60},
					{'method': 'popup', 'minutes': 10},
				],
			},
		}

		event = service.events().insert(calendarId='primary', body=event).execute()
		print ('Event created: %s' % (event.get('htmlLink')))
