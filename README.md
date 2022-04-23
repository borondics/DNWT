DNWT - Do Not Waste Time
====

A program to limit computer usage

Design principles:
- the project is not tied to any online service, the only requirement is to be able to see a public ICS calendar
- aim for one minute time resolution
- the script has to run every ~minute, even if the user is not logged in, so either a _demon_ or a _cron_ job of root
- the user should get nice visual notifications (preferably in their window manager native evironment)
- we should aim for nicely terminating sessions, no data loss - best is to lock the screen and then not let the user 
    log-in when not allowed, so run the script before the user session
- script configuration should be stored with no write right for the user
- project should live on GitHub with automations for
    - testing with unittests
    - make a pip package 
