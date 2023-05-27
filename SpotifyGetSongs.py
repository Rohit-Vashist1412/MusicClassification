import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, 
                                                                   client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def _split_uri(self,uri):
        'Takes the Spotify URL and splits it down to the URI which is needed for the API call'
        return uri.split('/')[-1].split('?')[0].split(':')[-1]


    def get_playlist_tracks(self,uri):
        'Easy function to return the playlist tracks as a dict'
        return self._transform_playlist_tracks(uri)
    

    def _fetch_playlist_tracks_json(self, uri):
        '''Function that takes the URI and makes a call to the spotify API to fetch the full JSON response.

        Returns a list of Json objects containing the required song data     
        
        '''
        uri = self._split_uri(uri)    
        offset = 0
        limit = 50
        json_list = []
        
        while True:
            items = self.sp.playlist_items(uri, offset=offset, limit=limit)
            json_list.append(items)
        
            if items['next']:
                offset += limit
            else:
                break
        
        return json_list
    
    def _transform_playlist_tracks(self,uri):

        ''' Transforms the Json response into a dict and returns the song name track id and artist name 
        
        Will add further metrics such as genre, BPM and length '''

        response  = self._fetch_playlist_tracks_json(uri)

        songs_dict = {'track_id': [], 'artist_name': [], 'song_name': []}

        for json in response:
             for item in json['items']:
                artist_name = [artist['name'] for artist in item['track']['album']['artists']]
                song_name = item['track']['name']
                track_id = item['track']['id']
                songs_dict['artist_name'].append(artist_name)
                songs_dict['song_name'].append(song_name)
                songs_dict['track_id'].append(track_id)

        return songs_dict
    
    
    def _fetch_new_release_json(self):
        '''Fetch the Json response of new album releases. Returns a list of json objects containing the albums recently released'''

        albums_list = []
        offset = 0
        limit = 50
        while True:
            albums = self.sp.new_releases(offset=offset, limit=limit)
            albums_list.append(albums)

            if albums['albums']['next']:
                offset += limit
            else:
                break

        return albums_list
    

    def _transform_new_releases_to_list(self):

        uri_list = []

        response_list = self._fetch_new_release_json() 

        for albums in response_list:
            for album in albums['albums']['items']:
                uri_list.append(album['uri'].split(':')[-1])
        
        return uri_list
                
    def get_new_releases(self):

        return self._transform_new_releases_to_list()        

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
