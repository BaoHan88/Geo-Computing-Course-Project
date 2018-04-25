# Community district based analysis
import csv
import json
import time
import shapely
from shapely.geometry import Point
from shapely.geometry import shape


# Community District Class
class District:

    def __init__(self, ID, Geometry, count):
        self.ID = ID # Community district ID, int
        self.Geometry = Geometry # shapely.multipolygon
        self.count = count


# Station class
class Station:

    def __init__(self, ID, lat, lng, count):
        self.ID = ID
        self.lat = lat
        self.lng = lng
        self.count = count


# Trip class
class Trip:

    def __init__(self, starttime, startstation, endtime, endstation):
        self.starttime = starttime
        self.startstation = startstation  # Station object
        self.endtime = endtime
        self.endstation = endstation  # Station object


# Read trip.csv file, into list of Trip object
# fh = open('/Users/yuchuanhuang/Git/Geog5541_Geocomputing_Project/Data/Sample10000.csv', 'r')
fh = open('/Users/yuchuanhuang/SPRING_2018/GEOG 5541 Principle of Geo-Computing/Project/201803_citibikenyc_tripdata.csv', 'r')
trips = csv.DictReader(fh)

Trip_list = []  # list of Trip object
# Search time bounds, changeable
search_time_lower = '2018-03-01 00:00:00'
search_time_upper = '2018-03-04 00:00:00'

for trip in trips:
    temp_starttime = time.mktime(time.strptime(trip['starttime'],'%Y-%m-%d %H:%M:%S'))
    if temp_starttime <= time.mktime(time.strptime(search_time_upper, "%Y-%m-%d %H:%M:%S")) and temp_starttime >= time.mktime(time.strptime(search_time_lower, "%Y-%m-%d %H:%M:%S")) :  # Append data before timestamp
        temp_endtime = time.mktime(time.strptime(trip['stoptime'],'%Y-%m-%d %H:%M:%S'))
        temp_startstation = Station(trip['start station id'], float(trip['start station latitude']), float(trip['start station longitude']), 0)
        temp_endstation = Station(trip['end station id'], float(trip['end station latitude']), float(trip['end station longitude']), 0)
        temp_trip = Trip(temp_starttime, temp_startstation, temp_endtime, temp_endstation)
        Trip_list.append(temp_trip)
    else:
        break

fh. close()
print('Trip file load completed')
print('%d trips input' % (len(Trip_list)))


# Read community district.geojson into class
fh = open('Data/Community Districts/Community Districts.geojson', 'r')
districts = json.load(fh)

Dist_list = []  # list of District object

for dist in districts['features']:
    dist_ID = int(dist['properties']['boro_cd'])
    dist_shape = dist['geometry']
    dist_polygon = shape(dist_shape)
    temp_dist = District(dist_ID, dist_polygon, 0)
    Dist_list.append(temp_dist)

fh.close()
print('Community district file load complete')
print('%d community districts found' % (len(Dist_list)))


# Count start station in each district
for trip in Trip_list:
    for dist in Dist_list:
        if Point(trip.startstation.lng, trip.startstation.lat).within(dist.Geometry):
            dist.count += 1

for dist in Dist_list:
    print(dist.ID, dist.count)