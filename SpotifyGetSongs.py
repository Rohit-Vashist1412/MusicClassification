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

    def get_playlist_tracks(self, uri):
        uri = uri.split('/')[-1].split('?')[0].split(':')[-1]
        songs_dict = {'track_id': [], 'artist_name': [], 'song_name': []}
        offset = 0
        limit = 50
        while True:
            items = self.sp.playlist_tracks(uri, offset=offset, limit=limit)

            for item in items['items']:
                artist_name = [artist['name'] for artist in item['track']['album']['artists']]
                song_name = item['track']['name']
                track_id = item['track']['id']
                songs_dict['artist_name'].append(artist_name)
                songs_dict['song_name'].append(song_name)
                songs_dict['track_id'].append(track_id)

            if items['next']:
                offset += limit
            else:
                break

        return songs_dict

    def pull_new_releases(self):
        uri_list = []
        offset = 0
        limit = 50
        while True:
            albums = self.sp.new_releases(offset=offset, limit=limit)
            for album in albums['albums']['items']:
                uri_list.append(album['uri'].split(':')[-1])
                
            if albums['albums']['next']:
                offset += limit
            else:
                break

        return uri_list

    def pull_album_tracks(self, uri_list):
        songs_dict = {'track_id': [], 'artist_name': [], 'song_name': []}
        uri_list = [uri.split('/')[-1].split('?')[0].split(':')[-1] for uri in uri_list]
        offset = 0
        limit = 20
        while True:
            items = self.sp.albums(uri_list[offset:offset + limit])

            for item in items['albums']:
                for track in item['tracks']['items']:
                    song_name = track['name']
                    track_id = track['id']
                    artist_name = [name['name'] for name in track['artists']]
                    songs_dict['track_id'].append(track_id)
                    songs_dict['song_name'].append(song_name)
                    songs_dict['artist_name'].append(artist_name)

            if len(uri_list) > offset + limit:
                offset += limit
            else:
                break

        return songs_dict
