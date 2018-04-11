import csv
import json
import fiona
import shapely
from shapely.geometry import Point
from shapely.geometry import shape

class District: # Community District Class

    def __init__(self, ID, Geometry, count):
        self.ID = ID # Community district ID, int
        self.Geometry = Geometry # shapely.multipolygon
        self.count = count


# Read trip CSV into list
fh_trip = open('/Users/yuchuanhuang/Git/Geog5541_Geocomputing_Project/Sample10000.csv', 'r')
dr_trip = csv.DictReader(fh_trip)

trip_count = 0
start_list = []
end_list = []
for trip in dr_trip:
    trip_count += 1
    temp_startpoint = Point(float(trip['start station longitude']), float(trip['start station latitude']))
    temp_endpoint = Point(float(trip['end station longitude']), float(trip['end station latitude']))
    start_list.append(temp_startpoint)
    end_list.append(temp_endpoint)

fh_trip.close()

# Read community district GEOJson into class
districts = json.load(open('/Users/yuchuanhuang/Git/Geog5541_Geocomputing_Project/Community Districts.geojson'))

dist_count = 0
dist_list = [] # list of District class

for dist in districts['features']:
    dist_count += 1
    dist_ID = int(dist['properties']['boro_cd'])
    dist_shape = dist['geometry']
    dist_polygon = shape(dist_shape)
    temp_dist = District(dist_ID, dist_polygon, 0)
    dist_list.append(temp_dist)


for start in start_list:
    for dist in dist_list:
        if start.within(dist.Geometry):
            dist.count += 1


for dist in dist_list:
    print(dist.ID, dist.count)