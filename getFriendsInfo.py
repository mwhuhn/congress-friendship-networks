# This collects friends' profile information

import tweepy
import sys
import time
import csv

ACCESS_TOKEN = # COPY FROM YOUR PROFILE
ACCESS_SECRET = # COPY FROM YOUR PROFILE
CONSUMER_KEY = # COPY FROM YOUR PROFILE
CONSUMER_SECRET = # COPY FROM YOUR PROFILE

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api = tweepy.API(auth)

for line in sys.stdin: # takes in rows of 100 friends' ids to lookup accounts
	row = line.split("|")
	row = map(int,row) # makes every id an integer
	while True:
		try:
			friendAccount = api.lookup_users(row)
			break
		except tweepy.TweepError:
			print >> sys.stderr, "Sleeping 15 getting friend info"
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break
	for friend in friendAccount:
		friendID = friend.id
		friendHandle = friend.screen_name.encode("ascii","ignore")
		friendCreateDate = str(friend.created_at.date())
		seq = (str(friendID),friendHandle,str(friendCreateDate))
		print "\t".join(seq)
