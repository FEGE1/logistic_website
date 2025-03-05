import googlemaps
from googlemaps import geocoding, directions, distance_matrix
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCylRnlEZdmLKjm1NzXZ5nO4RzvyNifhpk')

direction = distance_matrix.distance_matrix(gmaps,
                                  origins= "Çorlu Kervancı Rezidans",
                                  destinations= "izmit sadettin yalım caddesi Ege Market",
                                  mode='driving',
                                  language='tr',
                                  units='metric',
                                  departure_time=datetime.now(),
                                  traffic_model='best_guess')

print(direction)