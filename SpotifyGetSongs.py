import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

class SpotifyAPI:
    """
    A class for interacting with the Spotify Web API to retrieve playlist tracks, new releases, and album tracks.

    Args:
        client_id (str): Your Spotify application's client ID.
        client_secret (str): Your Spotify application's client secret.

    Attributes:
        client_id (str): Your Spotify application's client ID.
        client_secret (str): Your Spotify application's client secret.
        client_credentials_manager (spotipy.oauth2.SpotifyClientCredentials): Spotify client credentials manager.
        sp (spotipy.Spotify): Spotify API client instance.

    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, 
                                                                   client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def _split_uri(self, uri):
        """
        Extracts the Spotify track or playlist URI from a Spotify URL.

        Args:
            uri (str): Spotify URL.

        Returns:
            str: The Spotify track or playlist URI.

        """
        return uri.split('/')[-1].split('?')[0].split(':')[-1]

    def get_playlist_tracks(self, uri):
        """
        Retrieves tracks from a Spotify playlist.

        Args:
            uri (str): Spotify playlist URI.

        Returns:
            dict: Dictionary containing track information, including track_id, artist_name, and song_name.

        """
        return self._transform_playlist_tracks(uri)

    def _fetch_playlist_tracks_json(self, uri):
        """
        Fetches the JSON response of tracks from a Spotify playlist.

        Args:
            uri (str): Spotify playlist URI.

        Returns:
            list: List of JSON objects containing track data.
        """
        uri = self._split_uri(uri)    
        offset = 0
        limit = 50
        json_list = []
        
        while True:
            try:
                items = self.sp.playlist_items(uri, offset=offset, limit=limit)
                json_list.append(items)
                if items['next']:
                    offset += limit
                    time.sleep(0.1)  # Adding a small delay to avoid rate limiting
                else:
                    break
            except spotipy.SpotifyException as e:
                # Handle rate limiting or other API errors
                print("Error: ", e)
                break
        
        return json_list
    
    def _transform_playlist_tracks(self, uri):
        """
        Transforms the JSON response of playlist tracks into a dictionary.

        Args:
            uri (str): Spotify playlist URI.

        Returns:
            dict: Dictionary containing track information, including track_id, artist_name, and song_name.

        """
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
        """
        Fetches the JSON response of new album releases from Spotify.

        Returns:
            list: List of JSON objects containing information about recently released albums.

        """
        albums_list = []
        offset = 0
        limit = 50
        while True:
            try:
                albums = self.sp.new_releases(offset=offset, limit=limit)
                albums_list.append(albums)

                if albums['albums']['next']:
                    offset += limit
                    time.sleep(0.1)  # Adding a small delay to avoid rate limiting
                else:
                    break
            except spotipy.SpotifyException as e:
                # Handle rate limiting or other API errors
                print("Error: ", e)
                break

        return albums_list
    
    def _transform_new_releases_to_list(self):
        """
        Transforms the JSON response of new album releases into a list of album URIs.

        Returns:
            list: List of Spotify album URIs.

        """
        uri_list = []

        response_list = self._fetch_new_release_json() 

        for albums in response_list:
            for album in albums['albums']['items']:
                uri_list.append(album['uri'].split(':')[-1])
        
        return uri_list
                
    def get_new_releases(self):
        """
        Retrieves a list of new album releases on Spotify.

        Returns:
            list: List of Spotify album URIs.

        """
        return self._transform_new_releases_to_list()        

    def pull_album_tracks(self, uri_list):
        """
        Retrieves tracks from a list of Spotify album URIs.

        Args:
            uri_list (list): List of Spotify album URIs.

        Returns:
            dict: Dictionary containing track information, including track_id, artist_name, and song_name.
        """
        songs_dict = {'track_id': [], 'artist_name': [], 'song_name': []}
        uri_list = [self._split_uri for uri in uri_list]
        offset = 0
        limit = 20
        while True:
            try:  
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
                    time.sleep(0.1)
                else:
                    break
            except spotipy.SpotifyException as e:
                # Handle rate limiting or other API errors
                print("Error: ", e)
                break
            return songs_dict
