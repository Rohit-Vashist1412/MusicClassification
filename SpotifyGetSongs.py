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
        uri = self._extract_uri(uri)
        response = self._fetch_playlist_tracks(uri)
        return self._transform_playlist_tracks(response)

    def _extract_uri(self, uri):
        uri = uri.split('/')[-1].split('?')[0].split(':')[-1]
        return uri

    def _fetch_playlist_tracks(self, uri):
        offset = 0
        limit = 100
        tracks = []
        while True:
            response = self.sp.playlist_tracks(uri, offset=offset, limit=limit)
            tracks.extend(response['items'])
            if response['next']:
                offset += limit
            else:
                break
        return tracks

    def _transform_playlist_tracks(self, response):
        songs_dict = {'track_id': [], 'artist_name': [], 'song_name': []}
        for item in response:
            artist_name = [artist['name'] for artist in item['track']['album']['artists']]
            song_name = item['track']['name']
            track_id = item['track']['id']
            songs_dict['artist_name'].append(artist_name)
            songs_dict['song_name'].append(song_name)
            songs_dict['track_id'].append(track_id)
        return songs_dict

    def pull_new_releases(self):
        response = self._fetch_new_releases()
        return self._transform_new_releases(response)

    def _fetch_new_releases(self):
        uri_list = []
        offset = 0
        limit = 100
        while True:
            albums = self.sp.new_releases(offset=offset, limit=limit)
            uri_list.extend([album['uri'].split(':')[-1] for album in albums['albums']['items']])
            if albums['albums']['next']:
                offset += limit
            else:
                break
        return uri_list

    def _transform_new_releases(self, response):
        return response

    def pull_album_tracks(self, uri_list):
        response = self._fetch_album_tracks(uri_list)
        return self._transform_album_tracks(response)

    def _fetch_album_tracks(self, uri_list):
        uri_list = [uri.split('/')[-1].split('?')[0].split(':')[-1] for uri in uri_list]
        offset = 0
        limit = 100
        tracks = []
        while True:
            response = self.sp.albums(uri_list[offset:offset + limit])
            tracks.extend([track for album in response['albums'] for track in album['tracks']['items']])
            if len(uri_list) > offset + limit:
                offset += limit
            else:
                break
        return tracks

    def _transform_album_tracks(self, response):
        songs_dict = {'track_id': [], 'artist_name': [], 'song_name': []}
        for track in response:
            artist_name = [name['name'] for name in track['artists']]
            song_name = track['name']
            track_id = track['id']
            songs_dict['track_id'].append(track_id)
            songs_dict['song_name'].append(song_name)
            songs_dict['artist_name'].append(artist_name)
        return songs_dict
