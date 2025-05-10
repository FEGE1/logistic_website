import googlemaps
from googlemaps import geocoding, directions, distance_matrix
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCylRnlEZdmLKjm1NzXZ5nO4RzvyNifhpk')

def calculate_distance(origin, destination):
    
    direction = distance_matrix.distance_matrix(gmaps,
                                    origins= origin,
                                    destinations= destination,
                                    mode='driving',
                                    language='tr',
                                    units='metric',
                                    departure_time=datetime.now(),
                                    traffic_model='best_guess')

    return (direction['rows'][0]['elements'][0]['distance']['value'])/1000 # /1000 for translate metre to km