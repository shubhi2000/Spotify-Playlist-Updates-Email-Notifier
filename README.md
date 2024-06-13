# Spotify-Playlist-Updates-Email-Notifier

This code develops an application to send automated emails when you add/remove a track from your Spotify playlist. You will have to enter the email IDs of the followers you want to keep updated through this notification system. Twilio SendGrid is utilised to handle email delivery.

## Pre-requisites
Twilio SendGrid account \
Spotify Developer Account\
Python 3.6 or newer\
Ngrok

Install the python packages from the requirements.txt file using:
```
pip install -r requirements.txt
```

To run the code, you will have to configure the .env file with your credentials and redirect URI. Also, you'll need to update your email ID in line 108 of email_notifier.py.
