class order:
     def __init__(self,truck_id,status,receiving_loc,destination_loc):
          self.truck_id = truck_id
          self.status = status
          self.receiving_loc = receiving_loc
          self.destination_loc = destination_loc

class truck:
     def __init__(self,name,size):
          self.name = name
          self.size = size