import urllib2
UrlLink = "http://climate.weather.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=1840&EndYear=2015&Year=2015&Month=1&Day=28&selRowPerPage=100&cmdProvSubmit=Search"
aList = urllib2.urlopen(UrlLink).read().split("form action=\"/lib/climateData/Interform.php\" method=\"post\"")
removed = aList.pop(0)
item = aList[100]
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
temporyList = temporyList + hourlyValue
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
#print temporyList
#get latitude and longtitude
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
print UrlforStation