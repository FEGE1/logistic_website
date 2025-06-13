from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from order.models import Order, Truck
from order.map import Calculate_Distance

# Main()
def testFunc():

    Calculate_Orders()
    """
    order1 = Order.objects.get(id= 57)
    order2 = Order.objects.get(id= 58)

    print(Route_Limiter(order1, order2, 2))
    """

###################################################

def Check_Order_Is_Calculated(order_id):
    order = Order.objects.get(id=order_id)

    if order.truck is None:
        return False  # henüz hesaplanmamış

    return True  # tıra atanmış, hesaplanmış

        
    
def Route_Limiter(x, y, time_limit):
    x_receiving_address = x.receiving_location.address
    x_destination_address = x.destination_location.first().address
    
    y_receiving_address = y.receiving_location.address
    y_destination_address = y.destination_location.first().address

    return Calculate_Distance(x_receiving_address, x_destination_address, y_receiving_address, y_destination_address, time_limit)

# Calculate Algorithm

def Calculate_Orders():
    orders_by_size = Order.objects.select_related('cargo').order_by('-cargo__weight')
    waiting_list = []

    for order in orders_by_size:
        if hasattr(order,'cargo'):
            print(f'{order}: {order.cargo.weight}')
        
        else:
            print("weight değeri yok")
    
    for order in orders_by_size:
        if hasattr(order, 'truck'):
            if order.truck is None:
                waiting_list.append(order)

        else:
            print(f"{order} - This order doesn't have a truck ID ")
        

    if not Order.objects.filter(truck= None).exists():
        #messages.success(request, "✅ All orders are assigned to trucks.")
        print("✅ All orders are assigned to trucks.")
        return
    
    # To transfer trucks whose space values is the same as the order size value to the list
    for order in waiting_list:
        order_size = order.cargo.weight
        order_id = order.id

        trucks_ordered_by_space = Truck.objects.order_by("-space")

        trucks_same_space_with_order = []
        trucks_same_space_with_order_empty = []
        trucks_bigger_space_with_order=[]
        trucks_bigger_space_with_order_empty=[]
    
    # For equal truck space and order size
        for truck in trucks_ordered_by_space:
            if order_size == truck.space and truck.number_of_orders < 2:
                if truck.number_of_orders == 1:
                    trucks_same_space_with_order.append(truck)
                
                else:
                    trucks_same_space_with_order_empty.append(truck)
    # For bigger truck space than order size
        for truck in trucks_ordered_by_space:
            if order_size < truck.space and truck.number_of_orders < 2:
                if truck.number_of_orders == 1:
                    trucks_bigger_space_with_order.append(truck)
                
                else:
                    trucks_bigger_space_with_order_empty.append(truck)
        
    # ASSIGNMENT PROCESS
    if trucks_same_space_with_order:
        for truck in trucks_same_space_with_order:
            print("same space triggered")

            if truck.number_of_orders < 2 and not Check_Order_Is_Calculated(order_id):
                truck_id = truck.id
                order_in_truck = Order.objects.get(truck__id= truck_id)

                try:
                    if Route_Limiter(order, order_in_truck, 2):
                        print('Same space route limiter triggered')
                        
                        order.truck = truck
                        order.save()

                        truck.number_of_orders = (truck.number_of_orders)+1
                        truck.space = (truck.space)-(order.cargo.weight)
                        truck.save()

                        break
                except:
                    print(f"Hata: Tırdaki siparis bulunamadı\nTır ID:{truck_id}\nIslemdeki siparis ID: {order_id}")
    
    elif trucks_same_space_with_order_empty:
        for truck in trucks_same_space_with_order_empty:
            if truck.number_of_orders == 0 and not Check_Order_Is_Calculated(order_id):
                try:
                    order.truck = truck
                    order.save()

                    truck.number_of_orders = (truck.number_of_orders)+1
                    truck.space = (truck.space)-(order.cargo.weight)
                    truck.save()
                    break

                except:
                    print("Atama işleminde hata!")
    
    elif trucks_bigger_space_with_order:
        trucks_bigger_space_with_order.reverse()

        for truck in trucks_bigger_space_with_order:
            truck_space = truck.space

            if truck.number_of_orders < 2 and truck_space > order_size and not Check_Order_Is_Calculated(order_id):
                truck_id = truck.id 
                order_in_truck = Order.objects.get(truck__id= truck_id)

                try:
                    if Route_Limiter(order, order_in_truck, 2):
                        order.truck = truck
                        order.save()

                        truck.number_of_orders = (truck.number_of_orders)+1
                        truck.space = (truck.space)-(order.cargo.weight)
                        truck.save()
                        break

                except:
                    print("Hata: Tırdaki sipariş bulunamadı\nTır ID: {}\nİşlemdeki sipariş ID: {}".format(truck_id,order_id))

    elif trucks_bigger_space_with_order_empty:
        trucks_bigger_space_with_order_empty.reverse()

        for truck in trucks_bigger_space_with_order_empty:
            truck_space = truck.space

            if truck.number_of_orders == 0 and truck_space > order_size and not Check_Order_Is_Calculated(order_id):
                try:
                    order.truck = truck
                    order.save()

                    truck.number_of_orders = (truck.number_of_orders)+1
                    truck.space = (truck.space)-(order.cargo.weight)
                    truck.save()
                    break

                except:
                    print("Atama isleminde hata")
    
    else:
        print(f"❌ Order {order.id} hiçbir tıra atanamadı.")

##############################