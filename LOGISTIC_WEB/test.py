import googlemaps
from googlemaps import geocoding, directions, distance_matrix
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCylRnlEZdmLKjm1NzXZ5nO4RzvyNifhpk')

def Calculate_Multiple_Directions(origin, destination_1, destination_2, destination_3):
        direction = directions.directions(gmaps,
                                            origin= origin,
                                            destination= destination_3,
                                            waypoints= [destination_1, destination_2],
                                            mode='driving',
                                            language='tr',
                                            units='metric',
                                            departure_time=datetime.now(),
                                            traffic_model='best_guess')

        route = direction[0]
        total_distance = 0
        total_duration = 0

        for leg in route['legs']:
                total_distance += leg['distance']['value']
                total_duration += leg['duration']['value']

        print(f"total distance: {total_distance}\ntotal duration: {total_duration}")

Calculate_Multiple_Directions("çorlu","izmit","ankara","adana")