
# Getting Started

In order to show off what the [Summer of Context](http://summerofcontext.com) platform can do we're going to walk you through a short example app. 
This example app will show you how to use our REST API to retrieve user data from our platform. The basic workings of our REST API are explained [here](https://developer.summerofcontext.com/#/documentation#documentation_register_clientids).


The code contains valid credentials for a dummy account with realistic data so it should be trivial to run the sample and start experimenting.


### Declare imports and constants

```
import sys
import requests
import json

USER_ID = '51b81ea24d8fc6866c000005'
ACCESS_TOKEN = 'IDVisbLVpMEWNbX8Jap5iYF5mcAGf1Qd8M06ocin2xjCdaBYZn0ZTav8mk7LhstuSxiWo7XhQcZ2V5aCZHTu3Xi7dXQAPJloYd4zglXN3P5nnlIa9Mpb4cCi5PRwgpzO'
DATA_URL = 'http://argusdev3.arguslabs.be:3666/users/' + USER_ID + '/timeline?end=1377813600&limit=400&materialize=true&start=1377727200'
```

### Create the request and execute it

```
# prepare request

headers = {'authorization': 'Bearer ' + ACCESS_TOKEN, 'content-type': 'application/json'}

# execute request

r = requests.get(DATA_URL, headers=headers)

if (r.status_code != 200):
    print 'HTTP error: %d' % r.status_code
	    sys.exit(0)

js =  json.loads(r.content)
```

If the request succeeds, our API will return information from the user's timeline in a JSON format. An example of such a timeline response can be found in the [Timeline API reference](https://developer.summerofcontext.com/#/reference#timeline). json.loads will create a python object based on the JSON data.

### Parse the results

In the timeline response, the environment key contains a list of all [ContextItems](https://developer.summerofcontext.com/#/reference/#contextitems).
We'll filter out the music tracks and music sessions

```
# parse MusicTrackitems and LocationItems from the environment field in the response

musicItems = filter(lambda item: item['@type'] == 'ctx:MusicTrackItem', js['environment'])
locations = filter(lambda item: item['@type'] == 'ctx:LocationItem', js['environment'])

print 'found %d music items' % len(musicItems)
print 'found %d locations' % len(locations)
```

### Combine and show the context items

Now that we have lists of locations and music items, we can combine them to show which songs were listened to at each location.

```
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
```

A detailed description of all possible context items and their fields can be found in the [Data Model Reference](https://developer.summerofcontext.com/#/reference#data_model_reference)

### The results

If everything went according to plan, the output of the program should look like this.

```
User was at 51.216206,4.394491 from 2013-08-29T19:22:20.000+0200 to 2013-08-29T20:18:27.000+0200
    listened to Fall Out Boy - My Songs Know What You Did In The Dark (Light Em Up)
    listened to Tegan and Sara - Closer
User was at 51.216206,4.394491 from 2013-08-29T20:18:27.000+0200 to 2013-08-29T20:32:41.000+0200
    listened to Adele - Set Fire to the Rain
    listened to The Doors - Light My Fire
    listened to Justin Timberlake - Tunnel Vision
```





