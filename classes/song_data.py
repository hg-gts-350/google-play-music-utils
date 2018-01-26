class Track:
    def __init__(self, name):
        self.name = name
        self.artists = []
        self.releases = []

    def addArtist(self, artist):
        self.artists.append(artist)

    def addRelease(self, release):
        self.releases.append(release)

    def getReleases(self):
        return self.releases

    def getArtists(self):
    	return self.artists

    def getTrackInfo(self):
        return self.name + " - " + (" " if not self.artists else ", ".join(map(lambda a: a.getName(),self.artists)))

    def summary(self):
    	print self.getTrackInfo()

class Artist:
    def __init__(self, name):
        self.name = name

    def summary(self):
        print self.name

    def getName(self):
    	return self.name

class Release:
    def __init__(self, name):
        self.name = name

    def summary(self):
        print self.name

    def getName(self):
        return self.name
