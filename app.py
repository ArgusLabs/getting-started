import sys
import requests
import json

ACCESS_TOKEN = 'IDVisbLVpMEWNbX8Jap5iYF5mcAGf1Qd8M06ocin2xjCdaBYZn0ZTav8mk7LhstuSxiWo7XhQcZ2V5aCZHTu3Xi7dXQAPJloYd4zglXN3P5nnlIa9Mpb4cCi5PRwgpzO'
USER_ID = '51b81ea24d8fc6866c000005'

# Staging URL
url = 'http://argusdev3.arguslabs.be:3666/users/' + USER_ID + '/timeline?end=1376604000&limit=400&start=1376517600'
# TODO update to production URL
#url = 'http://api.summerofcontext.com:80/users/' + USER_ID + '/timeline?end=1376604000&limit=400&start=1376517600'

headers = {'authorization': 'Bearer ' + ACCESS_TOKEN, 'content-type': 'application/json'}

r = requests.get(url, headers=headers)

if (r.status_code != 200):
    print 'HTTP error: %d' % r.status_code
    sys.exit(0)

js =  json.loads(r.content)
print 'environment size: %d' % len(js['environment'])

musicItemCount = 0

musicHash = dict([(x['@id'],x) for x in js['environment']])

musicItems = filter(lambda item: item['@type'] == 'ctx:MusicTrackItem', js['environment'])
artists = map(lambda item: item['artist'].get('name', item['artist']['@id']), musicItems)
artists = list(set(artists))

musicSessions = filter(lambda item: item['@type'] == 'ctx:MusicSessionItem', js['environment'])

locations = filter(lambda item: item['@type'] == 'ctx:LocationItem', js['environment'])


print 'found %d music items' % len(musicItems)
print 'found %d artists' % len(artists)
print 'artists: %s' % artists
print 'found %d music sessions' % len(musicSessions)
print 'found %d locations' % len(locations)


sorted_locations = sorted(locations, key=lambda loc:loc['time']['timestamp'])

for i, location in enumerate(sorted_locations):
    start_time = location['time']['timestamp']
    if i < len(sorted_locations)-1:
        end_time = sorted_locations[i+1]['time']['timestamp']
        print 'at location x from %s to %s' % (start_time, end_time)
    
        musicTracksAtLocation = filter(lambda item: (item['time']['from']['timestamp'] > start_time and item['time']['from']['timestamp'] < end_time), musicItems)
        for musictrack in musicTracksAtLocation:
            print '\tlistened to %s' % musictrack['artist'].get('name',musictrack['artist']['@id'])










