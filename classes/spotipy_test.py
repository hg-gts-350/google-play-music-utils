import sys
import spotipy
import spotipy.util as util
import yaml

#token = util.prompt_for_user_token('XXX','playlist-read-private')

with open("playlist_reader.yaml", 'r') as ymlfile:
    print ymlfile
    cfg = yaml.safe_load(ymlfile)

for section in cfg:
  print section

#def show_tracks(tracks):
#  for i, item in enumerate(tracks['items']):
#    track = item['track']
#    print track['artists'][0]['name']+ " " + track['name']
#
#if token:
#  sp = spotipy.Spotify(token)
#  playlists = sp.user_playlists('triple.j.abc')
#  while playlists:
#    for i, playlist in enumerate(playlists['items']):
#      if playlist['name'] == 'The triple j Hitlist':
#        results = sp.user_playlist('triple.j.abc', playlist['id'],
#          fields="tracks,next")
#        tracks = results['tracks']
#        show_tracks(tracks)
#        while tracks['next']:
#          tracks = sp.next(tracks)
#          show_tracks(tracks)
#
#    if playlists['next']:
#      playlists = sp.next(playlists)
#    else:
#      playlists = None