from sclib import SoundcloudAPI, Track, Playlist
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# # Get the playlist using the URL/API
# playlist_url = os.environ.get('PLAYLIST_URL')
# api = SoundcloudAPI()
# playlist = api.resolve(playlist_url)

# # Check if the playlist is a Playlist object
# assert type(playlist) is Playlist

# # Iterate through the tracks in the playlist and download them
# for track in playlist.tracks:
#     filename = f'./test-album/{track.artist} - {track.title}.mp3'
#     with open(filename, 'wb+') as file:
#         track.write_mp3_to(file)

username = 'fiswi7etj3qmqt7tslv51it1c'
scope = 'user-library-read'  # Required scope for playlist access

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# playlists = sp.current_user_playlists()
# for playlist in playlists['items']:
#     print(f"Playlist: {playlist['name']} (ID: {playlist['id']})")

# Create a new playlist named "Test"
# playlist_name = 'Test'
# sp.user_playlist_create(username, name=playlist_name)

# print(f"Playlist '{playlist_name}' created successfully!")

# Get your liked songs
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])