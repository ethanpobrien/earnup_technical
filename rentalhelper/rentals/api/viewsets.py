import codecs
import csv
import math

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import RentalSerializer
from rentalhelper.rentals.models import Rental
from translation_dictionary import translation_dictionary
from landmarks import landmark_dict 

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        location_info = False
        search_string_info = False

        latitude= self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        dist = self.request.query_params.get('distance')
        query = self.request.query_params.get('query')

        ids_to_query = set()

        if longitude and latitude and dist:
            location_info = True
            try:
                location_dict = {
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'dist': float(dist),
                }
            except ValueError:
                location_info=False
            
            location_results = []
            run_count = 0

            # this while loop will expand the seearch distance if results
            # are not found within the requested distance
            while len(location_results) < 20:
                if run_count > 10:
                    break
                location_results = get_queryset_from_location_info(location_dict)
                location_dict['dist'] = 1.4*location_dict['dist']
                run_count += 1

            for ab_id in location_results:
                ids_to_query.add(ab_id)

        if query:
            search_string_info = True
            bedroom_count = get_bedroom_count(query)
            if bedroom_count > 0:
                queryset = queryset.filter(bedroom_count__gte=bedroom_count)
            landmark_point = get_landmark_results(query)
            if landmark_point:
                landmark_results = []
                run_count = 0

                landmark_loc_dict = {
                    'latitude': landmark_point[0],
                    'longitude': landmark_point[1],
                    'dist': 300,
                }

                while len(landmark_results) < 20:
                    if run_count > 10:
                        break
                    landmark_results = get_queryset_from_location_info(
                        landmark_loc_dict)
                    landmark_loc_dict['dist'] = 2*landmark_loc_dict['dist']
                    run_count += 1

                for ab_id in landmark_results:
                    ids_to_query.add(ab_id)

        queryset = queryset.filter(ab_id__in=ids_to_query)
        return queryset.order_by('-id')


def get_bedroom_count(text):
    for key in translation_dictionary.keys():
        if key in text:
            return translation_dictionary[key]
    return -1

def get_landmark_results(text):
    for key in landmark_dict.keys():
        if key in text:
            return landmark_dict[key]
    return None



def get_queryset_from_location_info(location_dict):
    lat = location_dict['latitude']
    lng = location_dict['longitude']
    dist = location_dict['dist']

    bbox = get_bbox(lat, lng, dist)
    csvreader = get_csv_reader()

    # build a list of IDs to fetch from DB by searching CSV
    found_rentals = []
    for row_count, row in enumerate(csvreader):
        try:
            row_lat = float(row[6])
            row_lng = float(row[7])
            row_point = [row_lat, row_lng]
            if check_in_bbox(bbox, row_point):
                found_rentals.append(row[0])
        except IndexError:
            # print('row skipped due to index error')
            pass
        except ValueError:
            # print('row skipped due to value error')
            pass

    return found_rentals




def get_bbox(lat, lng, dist):
    lat_shift = dist/111111
    lng_shift = -dist/(111111*math.cos(lat))

    lat_min = lat - lat_shift
    lat_max = lat + lat_shift

    lng_min = lng - lng_shift
    lng_max = lng + lng_shift

    return [lat_min, lat_max, lng_min, lng_max]


def check_in_bbox(bbox, point):
    lat = point[0]
    lng = point[1]
    if lat >= bbox[0] and lat <= bbox[1]:
        if lng >= bbox[2] and lng <= bbox[3]:
            return True
    return False

def get_csv_reader():
    filename = 'cleaned_file.csv'
    return csv.reader(codecs.open(filename, 'rU', 'utf-8'))


