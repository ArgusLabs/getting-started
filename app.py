import sys
import requests
import json

USER_ID = '51b81ea24d8fc6866c000005'
ACCESS_TOKEN = 'IDVisbLVpMEWNbX8Jap5iYF5mcAGf1Qd8M06ocin2xjCdaBYZn0ZTav8mk7LhstuSxiWo7XhQcZ2V5aCZHTu3Xi7dXQAPJloYd4zglXN3P5nnlIa9Mpb4cCi5PRwgpzO'
DATA_URL = 'http://argusdev3.arguslabs.be:3666/users/' + USER_ID + '/timeline?end=1377813600&limit=400&materialize=true&start=1377727200'

# parsing functions

def getArtistNameFromMusicTrackItem(item):
    event = item['based_on'][0]
    return event['product']['artist'].get('name', event['product']['artist']['@id'].split("/")[-1:][0].replace("+"," "))

def getTrackNameFromMusicTrackItem(item):
    event = item['based_on'][0]
    return event['product']['track'].get('name', event['product']['track']['@id'].split("/")[-1:][0].replace("+"," "))

def getLocationNameFromLocationItem(item):
    latitude = sorted_locations[i+1]['based_on'][0]['product']['place']['geo']['latitude']['float']
    longitude = sorted_locations[i+1]['based_on'][0]['product']['place']['geo']['longitude']['float']
    return "%f,%f" % (latitude, longitude)

# prepare request

headers = {'authorization': 'Bearer ' + ACCESS_TOKEN, 'content-type': 'application/json'}

# execute request

r = requests.get(DATA_URL, headers=headers)

if (r.status_code != 200):
    print 'HTTP error: %d' % r.status_code
    sys.exit(0)

js =  json.loads(r.content)

# parse MusicTrackitems and LocationItems from the environment field in the response

musicItems = filter(lambda item: item['@type'] == 'ctx:MusicTrackItem', js['environment'])
locations = filter(lambda item: item['@type'] == 'ctx:LocationItem', js['environment'])

print 'found %d music items' % len(musicItems)
print 'found %d locations' % len(locations)

# sort locations based on time

sorted_locations = sorted(locations, key=lambda loc:loc['time']['timestamp'])
musicTracksWithoutLocation = musicItems

# display locations with music tracks listened at that location

for i, location in enumerate(sorted_locations):
    start_time = location['time']['timestamp']
    if i < len(sorted_locations)-1:
        end_time = sorted_locations[i+1]['time']['timestamp']
        
        locationName = getLocationNameFromLocationItem(sorted_locations[i+1])
        print 'User was at %s from %s to %s' % (locationName, start_time, end_time)

        # filter music tracks between arrival and leaving time for this location
    
        musicTracksAtLocation = filter(lambda item: (item['time']['from']['timestamp'] > start_time and item['time']['from']['timestamp'] < end_time), musicTracksWithoutLocation)

        # display music tracks for this location

        for musictrack in musicTracksAtLocation:
            artist = getArtistNameFromMusicTrackItem(musictrack)
            track = getTrackNameFromMusicTrackItem(musictrack)

            print '\tlistened to %s - %s' % (artist, track)










