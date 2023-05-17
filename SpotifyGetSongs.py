import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, 
                                                                   client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)


    def get_playlist_tracks(self, URI):
        URI = URI.split('/')[-1].split('?')[0].split(':')[-1]
        songs_dict = {'track_id':[], 'artist_name':[], 'song_name':[]}
        items = self.sp.playlist_tracks(URI)

        for item in items['items']:
            artist_name = [artist['name'] for artist in item['track']['album']['artists']]
            song_name = item['track']['name']
            track_id = item['track']['id']
            songs_dict['artist_name'].append(artist_name)
            songs_dict['song_name'].append(song_name)
            songs_dict['track_id'].append(track_id)
        
        return songs_dict

    def pull_new_releases(self):
        URI_list = []
        albums = self.sp.new_releases()
        for album in albums['albums']['items']:
            URI_list.append(album['uri'].split(':')[-1])
            '''should add something to write new release ids to a file so
            when checking daily it only pulls data not already pulled'''
        
        return URI_list 

    def pull_album_tracks(self, URI_list):
        songs_dict = {'track_id':[], 'artist_name':[], 'song_name':[]}
        URI_list = [URI.split('/')[-1].split('?')[0].split(':')[-1] for URI in URI_list]
        items = self.sp.albums(URI_list)
        
        for item in items['albums']:
            for track in item['tracks']['items']:
                song_name = track['name']
                track_id = track['id']
                artist_name = [name['name'] for name in track['artists']] 
                songs_dict['track_id'].append(track_id)
                songs_dict['song_name'].append(song_name)
                songs_dict['artist_name'].append(artist_name)
        
        return songs_dict
