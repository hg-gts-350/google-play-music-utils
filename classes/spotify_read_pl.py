from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import yaml
import os

fn = os.path.join(os.path.dirname(__file__), 'playlist_reader.yaml')

class SpotifyPlayListReader:

  def __init__(self, yamlPath):
    with open(fn, 'r') as yamlfile:
      self.cfg = yaml.load(yamlfile)






def show_tracks(tracks):
  for i, item in enumerate(tracks['items']):
    track = item['track']
    print track['artists'][0]['name']+ " " + track['name']

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

for record in cfg:
  current_user = record['user']
  current_user_playlists = record['names']
  playlists = sp.user_playlists(current_user)
  while playlists:
    for i, playlist in enumerate(playlists['items']):
      if playlist['name'].upper() in map(str.upper, current_user_playlists):
        results = sp.user_playlist(current_user, playlist['id'], fields="tracks,next")
        tracks = results['tracks']
        show_tracks(tracks)
        while tracks['next']:
          tracks = sp.next(tracks)
          show_tracks(tracks)

    if playlists['next']:
      playlists = sp.next(playlists)
    else:
      playlists = None