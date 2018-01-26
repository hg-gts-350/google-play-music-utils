from gmusicapi import Mobileclient
from fuzzywuzzy import fuzz
from song_data import *

class GooglePlayPlaylistMaker:

	def __init__(self, api, name, description, date, tracks):
		self.api = api
		self.name = name
		self.description = description
		self.date = date
		self.tracks = tracks

	def __search_for_track__(self, track):
		artist_search_str = ""

		for index, artist in enumerate(track.getArtists()):
			artist_search_str = artist_search_str + artist.getName()
			if index < len(track.getArtists()):
				artist_search_str = artist_search_str + " "

		# We're only interested in the song results (not artists, podcasts etc.)
		song_name = track.name+ " " + artist_search_str
		print "Searching google for :" + song_name
		results = self.api.search(song_name)['song_hits']
		result_count = len(results)

		if result_count < 1:
			return None
		elif result_count == 1:
			return results[0]['track']['storeId']
		else:
			for result in results:
				for release in track.getReleases():
					if not release is None and fuzz.ratio(result['track']['album'],release.getName()) > 50:
						return result['track']['storeId']
			
	def create_or_update_playlist(self):
		song_ids=[]
		failed_tracks = {}
		playlist_id = None
		playlist_index = None
		missing_tracks = []

		for index, track in enumerate(self.tracks):

			song_id = self.__search_for_track__(track)

			if song_id is None:
				failed_tracks[index] = track
			else:
				song_ids.append(song_id)

		if failed_tracks:
			for rank in failed_tracks:
				missing_tracks.append("#"+str(rank)+" "+failed_tracks[rank].getTrackInfo())

		playlists = self.api.get_all_user_playlist_contents()

		for index, playlist in enumerate(playlists):
			if playlist['name'].startswith(self.name):
				playlist_id = playlist['id']
				playlist_index = index
				break

		final_description = self.description + (" " if not missing_tracks else " Missing tracks: "+",\n ".join(missing_tracks))
		playlist_name = self.name + " " + self.date.strftime("%d-%m-%Y")


		if(playlist_id is None):
			playlist_id = self.api.create_playlist(playlist_name, final_description)
		else:
			oldTracks = playlists[playlist_index]['tracks']
			ids_to_remove = map (lambda x: x['id'], oldTracks)
			self.api.remove_entries_from_playlist(ids_to_remove)
			self.api.edit_playlist(playlist_id, playlist_name, final_description)

		self.api.add_songs_to_playlist(playlist_id, song_ids)
