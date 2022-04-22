from turtle import down
from unittest import findTestCases
import arrow
from ics import Calendar, Event
import requests
import os
import time
import logging
import argparse
from glob import glob
'''
Design principles:
- the project is not tied to any online service, the only requirement is to be able to see a public ics calendar
- aim for one minute time resolution
- the script has to run every minute, even if the user is not logged in, so either a demon or a cron job of root
- the user should get nice visual notifications (preferably in their window manager native evironment)
- we should aim for nicely terminating sessions, no data loss - best is to lock the screen and then not let the user 
    log-in when not allowed, so run the script before the user session
- script configuration should be stored with a no write right for the user
- project shoud live on github with automations for
    - testing with unittests
    - make a pip package 
'''

# implement logging and debug messages

url = "https://calendar.google.com/calendar/ical/a7cqp125jldoq3mbg0ar05bqok%40group.calendar.google.com/private-135fbdf67b1f8439865c0726f6d418f9/basic.ics"
ical_text = requests.get(url).text

# TODO write the calendar to disk now - make sure to have the right user permissions
# keep only 10 copies for history

# this will be replaced by the url text when I have connection
with open('/Users/borondics/Downloads/event.ics', 'r') as f:
    ical_text = f.read()

fl = glob('/Users/borondics/Downloads/*.ics') # handle zero case
ftimes = []
ftimes.append([os.path.getctime(f) for f in fl])

# Delete the oldest calendar file if we would have more than 10
if len(fl)>9:
    oldest_existing_cal = fl[ftimes.index(min(ftimes))]
    os.remove(oldest_existing_cal)
    print(f'Limit of history reached, deleting oldest file. {oldest_existing_cal}')

s = arrow.utcnow().format('YYYY-MM-DD.HH-mm-ss.SS')
### handle fl empty case!
newest_existing_cal = fl[ftimes.index(max(ftimes))] # we need this only if the download fails try-else-except
next_cal_fname = 'mycal_'+s+'.ics'
wd = '/Users/borondics/Downloads/'

with open(wd+next_cal_fname, 'w') as f:
    print(f'Saving calendar to {next_cal_fname}')
    f.write(ical_text)

with open(wd+next_cal_fname, 'r') as f:
    print(f'reading {next_cal_fname}')
    ical_text = f.read()

############
# TODO check how ICAL handles recurring events
c = Calendar(ical_text)

allowed = False
for e in c.events:
    # TODO check how ICAL handles recurring events
    temp = e.begin<arrow.utcnow()<e.end
    # print(temp, arrow.utcnow(), e.begin, e.end)
    allowed+=temp

if allowed:
    print('Allowed')
elif not allowed:
    print('Not allowed')

## to lock the session: https://askubuntu.com/questions/184728/how-do-i-lock-the-screen-from-a-terminal
# use subprocess.run() from python
# https://unix.stackexchange.com/questions/291922/universal-way-to-logout-from-terminal-via-dbus

# or this: gdbus monitor -y -d org.freedesktop.login1 | grep LockedHint

# https://unix.stackexchange.com/questions/2881/show-a-notification-across-all-running-x-displays