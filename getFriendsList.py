# This takes people's ids in and outputs a csv
# of the ids and their friends' ids. Each friend
# is matched with the person.

import tweepy
import os
import csv
import time
import sys

ACCESS_TOKEN = # COPY FROM YOUR PROFILE
ACCESS_SECRET = # COPY FROM YOUR PROFILE
CONSUMER_KEY = # COPY FROM YOUR PROFILE
CONSUMER_SECRET = # COPY FROM YOUR PROFILE

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api = tweepy.API(auth)

def get_friends_ids(user_id):
	ids = []
	while True:
		time.sleep(60)
		for i, page in enumerate(tweepy.Cursor(api.friends_ids, id=user_id, count=5000).pages()):
			ids += page
			print >> sys.stderr, str(len(ids)) + " IDs collected"
			print >> sys.stderr, ids[len(ids)-1]
			time.sleep(60)
		break
	return ids


filename = # ADD YOUR FILE HERE
# file format:
# NID,"NAME","congHandle"
# where NID is a commonly-used ID for congressmen,
# and congHandle is the Twitter handle. Ex:
# N00004724,"SCHAKOWSKY, JANICE D","janschakowsky"

csvFile = open(filename)
csvReader = csv.reader(csvFile)

# final format to print:
# NID,congName,congHandle,congID,congName,congCreateDate,friendNum,friendHandle,friendID,friendName,friendCreateDate

for row in csvReader:
	congHandle = str(row[2])
	if len(congHandle) == 0: # handles congressmen with no Twitter handle
		print row[0] + "|" + row[1] + "|" + row[2] + "|||||"
		continue
	while True:
		try:
			person = api.get_user(congHandle)
			break
		except tweepy.TweepError:
			print >> sys.stderr, "Sleeping 15 getting user" + congHandle
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break
	congID = person.id
	congName = person.name.encode("ascii","ignore") # removes non-ascii characters
	congCreateDate = str(person.created_at.date()) # date account created
	friendList = get_friends_ids(congHandle)
	friendNum = len(friendList)
	for friend in friendList:
		seq = (row[0],row[1],row[2],str(congID),congName,str(congCreateDate),str(friendNum),str(friend))
		print "|".join(seq)
		friendNum -= 1 # last-added friend has highest number, used to identify order added

csvFile.close()
