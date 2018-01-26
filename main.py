#! /usr/bin/python2.7

import urllib2
import json
from classes.song_data import *
from classes.radio_api_reader import *
from classes.google_play_playlist_maker import *
from gmusicapi import Mobileclient
from datetime import datetime
from datetime import timedelta
import ConfigParser
import sys

try:
	config = ConfigParser.ConfigParser()
	config.read('conf.ini')

	user = config.get('google', 'user')
	code = config.get('google', 'app_code')

	yesterday = datetime.now() - timedelta(days=1)
	yesterday = yesterday.replace(hour=13, minute=00, second=00)
	aWeekAgo = yesterday - timedelta(days=7)
	theDayBeforeYesterday = yesterday - timedelta(days=1)

	triplejSevenDaysTracks = AbcRadioReader("triplej", "desc", 100, aWeekAgo, yesterday).parse_tracks()

	triplejMostPlayedYesterday = AbcRadioReader("triplej", "desc", 100, theDayBeforeYesterday, yesterday).parse_tracks()

	#-------- Search google play

	api = Mobileclient()
	logged_in = api.login(user, code, Mobileclient.FROM_MAC_ADDRESS)

	if not logged_in:
		raise ValueError('Could not login to google play music');

	base_name = "Triple J - Most Played (Over the past 7 days)"
	base_description = "Updated daily, in accordance with http://www.abc.net.au/triplej/featured-music/most-played/."
	mostPlayedLastSevenDays = GooglePlayPlaylistMaker(api, base_name, base_description, yesterday, triplejSevenDaysTracks)
	mostPlayedLastSevenDays.create_or_update_playlist()


	base_name = "Triple J - Most Played (Yesterday)"
	base_description = "Updated daily."
	mostPlayedLastSevenDays = GooglePlayPlaylistMaker(api, base_name, base_description, yesterday, triplejMostPlayedYesterday)
	mostPlayedLastSevenDays.create_or_update_playlist()

except Exception, e:
	print "Exception occurred, exiting"
	if logged_in:
		api.logout()
	sys.exit(1)
else:
	api.logout()