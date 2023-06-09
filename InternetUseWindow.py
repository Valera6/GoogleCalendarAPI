from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

days = 3
window = 10   #in minutes


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow()
        _from = now.replace(second=0, microsecond=0, minute=0, hour=now.hour) +datetime.timedelta(hours=1)
        for i in range(days*24):
            start = (_from + datetime.timedelta(hours=i)).isoformat()
            end = (_from + datetime.timedelta(hours=i, minutes=window)).isoformat()
            event = {
                  'summary': 'Internet Use Window',
                  'description': 'Description',
                  'start': {
                    'dateTime': start,
                    'timeZone': 'UTC'
                  },
                  'end': {
                    'dateTime': end,
                    'timeZone': 'UTC'
                  },
                  'recurrence': [
                    'RRULE:FREQ=DAILY;COUNT=1'
                  ],
                  'reminders': {
                    'useDefault': False,
                    'overrides': {'method': 'popup', 'minutes': 0}
                  },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            if i==days*24-1:
                print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print('\nAn error occurred: %s' % error)


if __name__ == '__main__':
    main()
