#-*-coding:utf-8 -*-
import csv, os, sys, time
from datetime import datetime

yoybase = "yoy"
lrrbase = "lrr"

def dealData(selectBase, notUseEntityData):
	data = readData("2016-04-09.csv")

	faultRange = []
	if bool(notUseEntityData) :
		pos = skipInvalidRecords(data)
		# print pos
		data = data[0:pos]


	for record in data:
	    if yoybase in selectBase:
	    	#print time, int(curval), int(yoyval)
	    	if isOverThreshold(int(record['curval']), int(record['yoyval'])):
	    		faultRange.append({"time": record['time'], 
	    			"deltaval": int(record['yoyval']) - int(record['curval']),
	    			"baseval": int(record['yoyval'])})
	    		# print record['time'], record['curval'], record['yoyval']
	    elif lrrbase in selectBase:
	    	#print time, curval, lrrval
	    	if isOverThreshold(int(record['curval']), int(record['lrrval'])):
	    		# print record['time'], record['curval'], record['lrrval']
	    		faultRange.append({"time": record['time'], 
	    			"deltaval": int(record['lrrval']) - int(record['curval']),
	    			"baseval": int(record['lrrval'])})
	    else:
	    	print time, curval, yoyval, lrrval	



	#print len(faultRange)
	calcAreaRatio(faultRange)


def skipInvalidRecords(data):
	pos = getCurrentTimePostion()
	while data[pos]['curval'] == "0" :
		pos = pos - 1
	return pos	

def readData(filepath):
	data = []
	reader = csv.reader(open(filepath))
	reader.next()
	for time, curval, yoyval, lrrval, in reader:
		tup = {"time": time, "curval": curval, "lrrval":lrrval, "yoyval": yoyval}
		data.append(tup)

	return data

def calcAreaRatio(faultData):
	startTime = time.strptime(faultData[0]["time"], "%H:%M:%S")
	a = 0
	b = 0
	lastTime = startTime

	for r in faultData[1: len(faultData)]:
		nextTime = time.strptime(r["time"], "%H:%M:%S")
		
		if (nextTime.tm_hour*60 + nextTime.tm_min - lastTime.tm_hour*60 - lastTime.tm_min) == 1:
			a = a + r["deltaval"]
			b = b + r["baseval"]
			#print r["time"]
			lastTime = nextTime
		else:
			if b > 0:
			    str = (u"下降比率:%d%%  时间段:%.2d:%.2d:%.2d - %.2d:%.2d:%.2d") % (a * 100 / b , startTime.tm_hour, startTime.tm_min, startTime.tm_sec, lastTime.tm_hour, lastTime.tm_min, lastTime.tm_sec)
			    print str
			
			a = 0
			b = 0
			startTime = nextTime
			lastTime = startTime

	if b > 0:
		str = (u"下降比率:%d%%  时间段:%.2d:%.2d:%.2d - %.2d:%.2d:%.2d") % (a * 100 / b , startTime.tm_hour, startTime.tm_min, startTime.tm_sec, lastTime.tm_hour, lastTime.tm_min, lastTime.tm_sec)
		print str

def getCurrentTimePostion():
	now = datetime.now()
	return now.hour * 60 + now.minute

def isOverThreshold(curval, cmpval):
	d = cmpval - curval
	return d > 0 and d*100/cmpval > 10


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "please input parameters: yoy or lrr"
	else:
		#print sys.argv[1]
		dealData(sys.argv[1], sys.argv[2])