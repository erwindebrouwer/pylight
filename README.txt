HUE-PYLIGHT
----------------------------------------------
The concept of this Python program is to get
the twilight (sunrise - sunset) times of any
given location. Using that times, this program
creates Linux cronjobs to turn a certain list
of Philips Hue lights ON and OFF.

> Author(s) : Erwin de Brouwer
> Version : 1.1

CREDITS
----------------------------------------------
https://sunrise-sunset.org/api
for providing the API connection to get the
sunrise - sunset) times of any given location.

VERSION INFO AND CHANGE LOG
----------------------------------------------
version | changes
1.0     | initial script to query times
1.1     | scheduling commands in Hue

SETUP
----------------------------------------------
1. Python modules required are:
   - requests
2. Configure and rename the sample 
   environment_settings.sample.py file to
   environment_settings.py
3. Create directories called "log" and "debug"
4. CRONJOB schedule the running of the script
   pylight.py to run just after midnight.
s
COMPONENTS
---------------------------------------------- 
> pylight.py
  base script to get and store the twilight 
  times and create the cronjobs
> environment_settings.py
  settings for the specific environment of
  installation.
> logfile
  place for the applications to write their
  log data to. Path and filename can be set
  in environment_settings.py.
> debugfile
  place for the applications to write their
  debug logging to. Path and filename can be
  set in environment_settings.py.
> pylight database (pylight_db.dict)
  text file containing a Python dictionary
  type text line for the application to
  store previous results data in.

