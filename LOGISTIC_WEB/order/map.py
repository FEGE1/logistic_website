import googlemaps
from googlemaps import geocoding, directions, distance_matrix
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCylRnlEZdmLKjm1NzXZ5nO4RzvyNifhpk')

def Calculate_Direction(origin, destination):

        direction = distance_matrix.distance_matrix(gmaps,
                                        origins= origin,
                                        destinations= destination,
                                        mode='driving',
                                        language='tr',
                                        units='metric',
                                        departure_time=datetime.now(),
                                        traffic_model='best_guess')

        distance_text = direction['rows'][0]['elements'][0]['distance']['text']
        distance_value = direction['rows'][0]['elements'][0]['distance']['value']/1000 # meter to km
        duration_text = direction['rows'][0]['elements'][0]['duration']['text']
        duration_value = direction['rows'][0]['elements'][0]['duration']['value']

        return ({'distance_text':distance_text, 'distance_value':distance_value, 'duration_text':duration_text, 'duration_value':duration_value})

def Calculate_Distance(x_receiving_address, x_destination_address, y_receiving_address, y_destination_address, time_limit):
    
    time_limit = time_limit*(60**2)

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
        
        # origin to final_dest
        route = direction[0]
        total_distance = 0
        total_duration = 0

        for leg in route['legs']:
                total_distance += leg['distance']['value']
                total_duration += leg['duration']['value']

        print(f"total distance: {total_distance}\ntotal duration: {total_duration}")

        return ({'origin': origin,
                 'distance_value':total_distance/1000,
                 'duration_value':total_duration})
    
    possibilities = [Calculate_Multiple_Directions(x_receiving_address, y_receiving_address, x_destination_address, y_destination_address),
                    Calculate_Multiple_Directions(x_receiving_address, y_receiving_address, y_destination_address, x_destination_address),
                    Calculate_Multiple_Directions(y_receiving_address, x_receiving_address, y_destination_address, x_destination_address),
                    Calculate_Multiple_Directions(y_receiving_address, x_receiving_address, x_destination_address, y_destination_address)]

    possibility_best = None

    for possibility in possibilities:
        if possibility_best is None:
            possibility_best = possibility
        
        else:
            if possibility['duration_value'] < possibility_best['duration_value']:
                possibility_best = possibility
    
    print(f"Best Duration is: {possibility_best['duration_value']} - time limit: {time_limit}")

    # Limit control section

    if possibility_best['origin'] == x_receiving_address:
        order_duration = Calculate_Direction(x_receiving_address, x_destination_address)['duration_value']

        if abs(order_duration - possibility_best['duration_value']) <= time_limit:
            print("Sapma:  "+str(abs(order_duration - possibility_best['duration_value'])))
            return True

        else:
            print("Sapma:  "+str(abs(order_duration - possibility_best['duration_value'])))
            return False
    
    elif possibility_best['origin'] == y_receiving_address:
        order_duration = Calculate_Direction(y_receiving_address, y_destination_address)['duration_value']

        if abs(order_duration - possibility_best['duration_value']) <= time_limit:
            print("Sapma:  "+str(abs(order_duration - possibility_best['duration_value'])))
            return True

        else:
            print("Sapma:  "+str(abs(order_duration - possibility_best['duration_value'])))
            return False
        
    else:
        print("Time limit func ERROR!")

# print(Calculate_Distance('çorlu','adana','izmit','ankara',2))