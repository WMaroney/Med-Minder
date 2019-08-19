from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import timedelta
from __future__ import print_function
from httplib2 import Http
from oauth2client import file, client, tools

#pip install google-api python-client

scopes = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
credentials = flow.run_console()

pickle.dump(creditials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))

service = build("calendar", "v3", credentials=crediatls)

result = service.calendarList().list().execute()

calendar_id = result['items'][0]['id']
result = service.events().list(calendarId=calendar_id).execute()
print(result['items'][0])

def create_event(start_time_str, summary, duration=1, attendees=None, description=None, location=None):
	matches = list(datefinder.find_dates(start_time_str))
	if len(matches):
		start_time = matches[0]
		end_time = start_time + timedelta(hours=duration)
	event = {
			'summary': 'Test for Med-Minder',
			'description': 'A chance to hear more about Google\'s developer products.',
			'start': {
				'dateTime': Mydate,
				'timeZone': 'America/New_York',
			},
			'end': {
				'dateTime': Mydate1,
				'timeZone': 'America/New_York',
			},
			'recurrence': [
				'RRULE:FREQ=DAILY;COUNT=1'
			],
			'reminders': {
				'useDefault': False,
				'overrides': [
					{'method': 'email', 'minutes': 24 * 60},
					{'method': 'popup', 'minutes': 10},
				],
			},
		}
	pp.pprint('''*** %r event added:
	With: %s
	Start: %s
	End:	%s''' % (summary.encode('utf-8'),
		attendees, start_time, end_time))
	return service.events().insert(calndarId='primary',
	body=event,sendNotifications=True).execute()	

create_event(start_time_str, summary [, duration [, attendees [, description [, location ]]]])
