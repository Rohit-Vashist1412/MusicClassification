import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()

def get_tracks(URI):
# Get URI in proper format for API
    URI = URI.split(',')[-1].split('?')[0]
    
    songs = {'artistName':[],'songName':[]}
    
    #Auth uses env vars
    client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("sp_client_id"), 
    client_secret=os.getenv("sp_client_secret"))
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    items = sp.playlist_tracks('37i9dQZF1DXcBWIGoYBM5M')

    for item in items['items']:
        artistName = [artist['name'] for artist in item['track']['album']['artists']]
        songName = item['track']['name']
        songs['artistName'].append(artistName)
        songs['songName'].append(songName)
    return songs
