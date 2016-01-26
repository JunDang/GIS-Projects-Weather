import urllib2, time
UrlLink = "http://climate.weather.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=1840&EndYear=2015&Year=2015&Month=1&Day=28&selRowPerPage=100&cmdProvSubmit=Search"
aList = urllib2.urlopen(UrlLink).read().split("form action=\"/lib/climateData/Interform.php\" method=\"post\"")
removed = aList.pop(0)
print aList
#print aList[-1]