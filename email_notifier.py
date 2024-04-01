# module imports
from fastapi import FastAPI, HTTPException  
import requests  
import os  
from dotenv import load_dotenv  

# Load environment variables from .env file
load_dotenv()

# Create a FastAPI application instance
app = FastAPI()

# Spotify settings
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")  # Get Spotify client ID from environment variables
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")  # Get Spotify client secret from environment variables

# Endpoint to add a track to a playlist
@app.post("/add_track/")
def add_track_to_playlist(playlist_id:str, track_id:str, followers: str):
    """
    track_id: id of the track from Spotify URL
    playlist_id: id of the playlist from Spotify URL
    followers: space-separated email ID of followers
    """
    # Read access token from file
    with open("access_token.txt", "r") as file:
        access_token = file.read()
    
    # Define headers with access token for Spotify API authorization
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Add track to playlist using Spotify API
    response = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json={"uris": ["spotify:track:" + track_id]})
    
    # If track added successfully, send confirmation email to followers
    if response.status_code == 201:
        # Get track name from Spotify API response
        response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
        track_name = response.json()['name']
        
        # Get playlist name from Spotify API response
        response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers)
        playlist_name = response.json()['name']
        
        # Send confirmation email
        send_confirmation_email(f"Track {track_name} added to the playlist {playlist_name}.", followers)
        
        # Return success message
        return {"message": "Track added successfully."}
    else:
        # Raise exception if track addition fails
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Endpoint to remove a track from a playlist
@app.post("/remove_track/")
def remove_track_from_playlist(playlist_id:str, track_id:str, followers:str):
    """
    track_id: id of the track from Spotify URL
    playlist_id: id of the playlist from Spotify URL
    followers: space-separated email ID of followers
    """
    # Read access token from file
    with open("access_token.txt", "r") as file:
        access_token = file.read()
    
    # Define headers with access token for Spotify API authorization
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Remove track from playlist using Spotify API
    response = requests.delete(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json={"tracks": [{"uri": "spotify:track:" + track_id}]})
    
    # If track removed successfully, send confirmation email to followers
    if response.status_code == 200:
        # Get track name from Spotify API response
        response = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=headers)
        track_name = response.json()['name']
        
        # Get playlist name from Spotify API response
        response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers)
        playlist_name = response.json()['name']
        
        # Send confirmation email
        send_confirmation_email(f"Track {track_name} added to the playlist {playlist_name}.", followers)
        
        # Return success message
        return {"message": "Track added successfully."}
    else:
        # Raise exception if track addition fails
        raise HTTPException(status_code=response.status_code, detail=response.text)

# SendGrid settings
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_SEND_EMAIL_URL = "https://api.sendgrid.com/v3/mail/send"

def send_confirmation_email(message, followers):
    # Extract email IDs by splitting at spaces
    followers = followers.split(" ")

    # Set authorization header for SendGrid API access
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}"
    }

    # Format emails for personalizations
    emails = []
    for email in followers:
        emails.append({"email": email})

    # Define email settings
    payload = {
        "personalizations": [{"to": emails}],
        "from": {"email": <YOUR_EMAIL_ID>},
        "subject": "Spotify Playlist Update Notification",
        "content": [{"type": "text/plain", "value": message}]
    }

    # Send email
    response = requests.post(SENDGRID_SEND_EMAIL_URL, headers=headers, json=payload)

    # Verify success (status code 202)
    if response.status_code != 202:
        raise HTTPException(status_code=response.status_code, detail=response.text)
