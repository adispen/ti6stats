import requests
import sys
import time
import urllib
from datetime import datetime
from pymongo import MongoClient

client = MongoClient()
db = client.stats

def insertStream(now, viewers, stream, gameName, streamTitle, rank, saveName):
	exists = db.streams.find({"name" : stream})
	if exists.count() == 0:
		db.streams.insert_one(
			{
				"name": stream,
				"stats": [
					{
						"time": now,
						"viewers": viewers,
						"title": streamTitle,
						"game": gameName,
						"rank": rank,
			#			"preview": saveName
					}
				]
			}
		)
	else:
		newStat = {
				"time": now,
				"viewers": viewers,
				"title": streamTitle,
				"game": gameName,
				"rank": rank,
		#		"preview": saveName
				}
		db.streams.update_one({"name" : stream}, {"$push" : {"stats" : newStat}})

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
			for i, streamObj in enumerate(content['streams']):
				viewers = content['streams'][i]['viewers']
				stream = content['streams'][i]['channel']['display_name']
				gameName = content['streams'][i]['game']
				streamTitle = content['streams'][i]['channel']['status']
				saveName = "images/" + str(stream) + str(now) + ".jpg"
			#	image = urllib.URLopener()
			#	image.retrieve(content['streams'][i]['preview']['large'], saveName)
				insertStream(now, viewers, stream, gameName, streamTitle, i+1, saveName)
				print "#" + str(i+1) + " "  + str(viewers) + " watching " + stream + " play " +  gameName + " at " + now + " " + streamTitle
		time.sleep(300)

def main():
	getTop()

main()
