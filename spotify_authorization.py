import requests  
import os  
from dotenv import load_dotenv  

# load environment variables from .env file
load_dotenv() 

# Retrieve Spotify application details from environment variables
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Scopes required by your application
SCOPES = ['playlist-modify-private%20playlist-modify-public']

# Construct authorization URL
auth_params = {
	'response_type': 'code',
	'client_id': CLIENT_ID,
	'scope': ' '.join(SCOPES),
	'redirect_uri': REDIRECT_URI
}

# Create authorization URL
auth_url = f'https://accounts.spotify.com/authorize?{"&".join([f"{k}={v}" for k, v in auth_params.items()])}'  

# Redirect user to Spotify authorization page
print('Please go to the following URL and authorize access:')
print(auth_url)

# After user authorizes the application, Spotify will redirect back to REDIRECT_URI with authorization code

# Handle authorization code
authorization_code = input('Enter the authorization code from the callback URL: ')

# Exchange authorization code for access token
token_params = {
	'grant_type': 'authorization_code',
	'code': authorization_code,
	'redirect_uri': REDIRECT_URI,
	'client_id': CLIENT_ID,
	'client_secret': CLIENT_SECRET
}

# Request access token
token_response = requests.post( 'https://accounts.spotify.com/api/token', data=token_params) 
access_token = token_response.json()['access_token']  # Extract access token

with open("access_token.txt", "w") as file:
	file.write(access_token)  # Write access token to file
