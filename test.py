import urllib2, time
UrlLink = "http://climate.weather.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=1840&EndYear=2015&Year=2015&Month=1&Day=28&selRowPerPage=100&cmdProvSubmit=Search"
aList = urllib2.urlopen(UrlLink).read().split("form action=\"/lib/climateData/Interform.php\" method=\"post\"")
removed = aList.pop(0)
#print '============================'

for item in aList:
	temporyList = []
	hourlyRangeIndex = item.find('hlyRange')
	tempofh = item[(hourlyRangeIndex+17):]
	#print tempofh
	startIndexHourlyRange = hourlyRangeIndex + 17
	endIndexHourlyRange = tempofh.find('"') + startIndexHourlyRange
	hourlyRange = item[startIndexHourlyRange: endIndexHourlyRange]
	hourlyValue = hourlyRange.split("|")
	temporyList = temporyList + hourlyValue
	startIndexDailyRange = item.find('dlyRange') + 17
	tempofd = item[startIndexDailyRange:]
	endIndexDailyRange = tempofd.find('"') + startIndexDailyRange
	dailyRange = item[startIndexDailyRange: endIndexDailyRange]
	dailyValue = dailyRange.split("|")
	#print "dailyValue: " + str(dailyValue)
	temporyList = temporyList + dailyValue
	#print hourlyValue
	#print temporyList
	monthlyRangeIndex = item.find('mlyRange')
	tempofm = item[(monthlyRangeIndex+17):]
	#print tempofm
	startIndexMonthlyRange = monthlyRangeIndex + 17
	endIndexMonthlyRange = tempofm.find('"') + startIndexMonthlyRange
	#print endIndexMonthlyRange
	monthlyRange = item[startIndexMonthlyRange: endIndexMonthlyRange]
	#print monthlyRange
	monthlyValue = monthlyRange.split("|")
	#print monthlyValue
	temporyList = temporyList + monthlyValue
	#print "temporyList: " + str(temporyList)
	StationidIndex = item.find("StationID")
	tempofStationid = item[(StationidIndex + 18):]
	startIndexStationid = StationidIndex + 18
	endIndexStationid = tempofStationid.find('"') + startIndexStationid
	StationidValue = item[startIndexStationid:endIndexStationid]
	#print "StationidValue: " + str(StationidValue)
	#temporyList = temporyList.append(StationidValue) 
	temporyList.append(StationidValue)
	#print "temporyList: " + str(temporyList)
	StartIndexStationName = item.find('wordWrap') + 10
	tempofSName = item[StartIndexStationName:]
	endIndexStationName = tempofSName.find('<') - 1 + StartIndexStationName
	StationNameValue = item[StartIndexStationName: endIndexStationName + 1].strip()
	print StationNameValue
	temporyList.append(StationNameValue)
	time.sleep(3)
	yearmonthday = dailyValue[1].split("-")
	yearmonthday2 = hourlyValue[1].split("-")
	if dailyValue[1] != '':
		Year = yearmonthday[0]
		Month = int(yearmonthday[1])
		Day = "01"
		UrlforStation = "http://climate.weather.gc.ca/climateData/dailydata_e.html?timeframe=2&Prov=ON&StationID=" + str(StationidValue) + "&dlyRange=" + str(dailyRange) +"&Year=" + str(Year) + "&Month=" + str(Month) + "&Day=" + str(Day)
	else:
		Year = yearmonthday2[0]
		Month = int(yearmonthday2[1])
		Day = int(yearmonthday2[2])
		UrlforStation = "http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=ON&StationID=" + str(StationidValue) + "&hlyRange=" + str(hourlyRange) +"&Year=" + str(Year) + "&Month=" + str(Month) + "&Day=" + str(Day)
	rowinUrl = urllib2.urlopen(UrlforStation).read()
	StartIndexofFirstTable = rowinUrl.find("<table")
	EndIndexofFirstTable = rowinUrl.find("</table>")
	tablecontent = rowinUrl[StartIndexofFirstTable: EndIndexofFirstTable + 1]
	#print tablecontent
	workrow = tablecontent.split("<tr>")
	removed = workrow.pop(0)
	secondrow = workrow[1]
	secondList = secondrow.split("<td>")
	secondList.pop(0)
	#find degree
	element1 = secondList[0]
	EndIndexLatDegree = element1.find("<abbr title=\"degrees\">")
	LatDegree = element1[0: EndIndexLatDegree].strip()
	convertedLatDegree = float(LatDegree)
	#find minute
	EndIndexLatMin = element1.find("<abbr title=\"minute\">")
	StartIndexLatMin = EndIndexLatMin - 2
	LatMin = element1[StartIndexLatMin: EndIndexLatMin].strip()
	convertedLatMin = float(LatMin) / 60
	#find second
	EndIndexLatSec = element1.find("<abbr title=\"second\">")
	StartIndexLatSec = EndIndexLatSec - 6
	LatSec = element1[StartIndexLatSec: EndIndexLatSec].strip()
	convertedLatSec = float(LatSec) / 3600
	#find latitude
	Latitude = convertedLatDegree + convertedLatMin + convertedLatSec
	temporyList.append(Latitude)
	#print Latitude
	#Find longitude. 1. find degree
	element2 = secondList[1]
	EndIndexLonDegree = element2.find("<abbr title=\"degrees\">")
	LonDegree = element2[0: EndIndexLonDegree].strip()
	convertedLonDegree = float(LonDegree)
	#find minute
	EndIndexLonMin = element2.find("<abbr title=\"minute\">")
	StartIndexLonMin = EndIndexLonMin - 2
	LonMin = element2[StartIndexLonMin: EndIndexLonMin].strip()
	convertedLonMin = float(LonMin) / 60
	#find second
	EndIndexLonSec = element2.find("<abbr title=\"second\">")
	StartIndexLonSec = EndIndexLonSec - 6
	LonSec = element2[StartIndexLonSec: EndIndexLonSec].strip()
	convertedLonSec = float(LonSec) / 3600
	#find lontitude
	Longitude = convertedLonDegree + convertedLonMin + convertedLonSec
	temporyList.append(Longitude)
	#get elevation
	element3 = secondList[2]
	EndIndexElevation = element3.find("<abbr title=\"meter\">")
	elevation = element3[0: EndIndexElevation].strip()
	temporyList.append(elevation)
	thirdrow = workrow[2]
	thirdlist = thirdrow.split("<td>")
	thirdlist.pop(0)
	#get climate ID
	element4 = thirdlist[0]
	EndIndexID = element4.find("</td>")
	ClimateID = element4[0: EndIndexID].strip()
	temporyList.append(ClimateID)
	#get WMO ID
	element5 = thirdlist[1]
	EndIndexWMO = element5.find("</td>")
	WMOID = element5[0:EndIndexWMO].strip()
	temporyList.append(WMOID)
	#get TC ID
	element6 = thirdlist[2]
	EndIndexTCID= element6.find("</td>")
	TCID = element6[0:EndIndexTCID].strip()
	temporyList.append(TCID)
	print temporyList
	

	
	
	
	
#print aList
