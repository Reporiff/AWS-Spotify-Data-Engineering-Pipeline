import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3

def lambda_handler(event, context):
    
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DXa8NOEUWPn9W?si=28c19eb0023b4058"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    
    data = sp.playlist_tracks(playlist_URI)
    
    client = boto3.client('s3')
    
    filename = "spotify_raw_122334" + ".json"
    
    client.put_object(
             Bucket="spotifyetl-de-project",
             Key="raw_data/to_process/" + filename,
             Body=json.dumps(data)
             )

