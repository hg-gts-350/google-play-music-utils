import urllib2
import urllib
import json
from datetime import datetime
from song_data import *

class AbcRadioReader:

	__radio_url__ = "https://music.abcradio.net.au/api/v1/recordings/plays.json?"

	def __init__(self, service, order, limit, startDate, endDate):
		self.service = service
		self.order = order
		self.limit = limit
		self.startDate = startDate
		self.endDate = endDate

	def __build_params__(self):
		params = {}
		params ['service'] = self.service
		params ['order'] = self.order
		params ['limit'] = str(self.limit)
		params ['from'] = self.startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
		params ['to'] = self.endDate.strftime("%Y-%m-%dT%H:%M:%SZ")

		return params

	def get_tracks(self):
		# example url "https://music.abcradio.net.au/api/v1/recordings/plays.json?order=desc&limit=50&service=triplej&from=2018-01-13T13:00:00Z&to=2018-01-20T13:00:00Z"
		params = self.__build_params__()
		# doesnt like url encoding ?
		queryString = '&'.join(["{}={}".format(k, v) for k, v in params.items()])
		url = AbcRadioReader.__radio_url__+queryString
		print url
		req = urllib2.Request(url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		return json.loads(f.read())

	def parse_tracks(self):
		trackJson = self.get_tracks()
		tracks = []

		for song in trackJson['items']:

			track = Track(song['title'])
			
			for artist in song['artists']:
				track.addArtist(Artist(artist['name']))

			for release in song['releases']:
				track.addRelease(Release(release['title'])) 

			tracks.append(track)

		return tracks