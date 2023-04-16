import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("sp_client_id"), 
client_secret=os.getenv("sp_client_secret"))
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

