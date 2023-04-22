import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
#Auth uses env vars

client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("sp_client_id"), 
client_secret=os.getenv("sp_client_secret"))
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_tracks(URI):
# Get URI in proper format for API
    URI = URI.split('/')[-1].split('?')[0].split(':')[-1]
    
    songs_dict = {'track_id':[],'artist_name':[],'song_name':[]}
    
    items = sp.playlist_tracks(URI)

    for item in items['items']:
        artist_name = [artist['name'] for artist in item['track']['album']['artists']]
        song_name = item['track']['name']
        track_id = item['track']['id']
        songs_dict['artist_name'].append(artist_name)
        songs_dict['song_name'].append(song_name)
        songs_dict['track_id'].append(track_id)
    return songs_dict


def pull_new_releases():
    URI_list = []
    albums = sp.new_releases()
    for album in albums['albums']['items']:
         URI_list.append(album['uri'].split(':')[-1])
         '''should add something to write new release ids to a file so
         when checking daily it only pulls data not already pulled''' 

    return URI_list 

##Albums and playlist data are stored differently so write an alternate func to pull album data 

def pull_album_tracks(URI_list):

    songs_dict = {'track_id':[],'artist_name':[],'song_name':[]}
    URI_list = [URI.split('/')[-1].split('?')[0].split(':')[-1] for URI in URI_list]
    items = sp.albums(URI_list)
    
    for item in items['albums']:
        for track in item['tracks']['items']:
            song_name = track['name']
            track_id = track['id']
            artist_name = [name['name'] for name in track['artists']] 
            songs_dict['track_id'].append(track_id)
            songs_dict['song_name'].append(song_name)
            songs_dict['artist_name'].append(artist_name)
    return songs_dict

