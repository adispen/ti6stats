import requests
import sys
import time
import urllib
from datetime import datetime


def getTop():
	url = "https://api.twitch.tv/kraken/streams?game=dota%202"
	while True:
		r = requests.get(url)
		content = r.json()
		if not content['streams']:
			print "Either nobody is playing " + game + " or it is not a valid game"
			return
		else:
			nowFull = datetime.now()
			now = nowFull.strftime('%Y-%m-%d %H:%M:%S')
			#for i, streamObj in enumerate(content['streams']):
			i = 0
			viewers = content['streams'][i]['viewers']
			stream = content['streams'][i]['channel']['display_name']
			gameName = content['streams'][i]['game']
			streamTitle = content['streams'][i]['channel']['status']
			
			print "#" + str(i+1) + " "  + str(viewers) + " watching " + stream + " play " +  gameName + " at " + now + " " + streamTitle
		time.sleep(60)

getTop()
