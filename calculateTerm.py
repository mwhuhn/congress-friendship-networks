# This calculates the term the friend was added
# by the congressman.
# Must use data where friends are listed in order
# they were added (first to most recent).

import time
import sys

ID = ""
session = 0  # starts session before 110th Congress
date = time.strptime("2005-01-01","%Y-%m-%d")
date0 = time.strptime("2007-01-04","%Y-%m-%d")
date1 = time.strptime("2009-01-06","%Y-%m-%d")
date2 = time.strptime("2011-01-05","%Y-%m-%d")
date3 = time.strptime("2013-01-03","%Y-%m-%d")
date4 = time.strptime("2015-01-06","%Y-%m-%d")

def getMinSession(date):
	"""get session of congress based on date"""
	if date < date0:
		return 0
	elif date < date1:
		return 1
	elif date < date2:
		return 2
	elif date < date3:
		return 3
	elif date < date4:
		return 4
	else:
		return 5


# input data format: (tab-separated)
# NID CNAME CHANDLE CTID CTNAME CDATE FNUM FTID FHANDLE FDATE
# 0   1     2       3    4      5     6    7    8       9

for row in sys.stdin:
	row = row.rstrip().split("\t") # change split if you use don't separate by tabs
	CTID = row[3]
	CDATE = time.strptime(row[5],"%Y-%m-%d")
	FTID = row[7]
	FDATE = time.strptime(row[9],"%Y-%m-%d")
	CSESSION = getMinSession(CDATE)
	if CTID != ID: # checks if there is a new congressmen, if so, reset session
		print >> sys.stderr, "changing id"
		ID = CTID
		date = CDATE
		session = CSESSION
	FSESSION = getMinSession(FDATE)
	# if the friend was added in a session after the current session, move session forward
	if FSESSION > session: 
		session = FSESSION
	for i in range(session,5):
		line = row + [str(i)]
		print "\t".join(line)
