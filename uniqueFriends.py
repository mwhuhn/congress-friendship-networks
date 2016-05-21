# This creates rows of 100 friend ids to
# lookup account information for. The
# Twitter API allows you to look up 100
# at a time so this format makes the
# process faster.

import sys
import csv

csvFile = open("friends.csv")
csvReader = csv.reader(csvFile, delimiter="|")

friends = [] # stores all friends
temp = [] # stores next 100 friends to print

for row in csvReader:
	fID = str(row[7])
	if len(fID) > 0:
		if fID not in friends:
			friends.append(fID)
			if len(temp) < 100:
				temp.append(fID)
			else:
				print temp # prints completed row
				temp = [] # temp empties
				temp.append(fID) # add first new entry
print temp

