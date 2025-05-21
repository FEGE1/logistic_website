from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from order.models import Order, Truck

def testFunc():
    """
    orders = Order.objects.all()
    i=0
    for order in orders:
        if hasattr(order, 'truck'):
            print(f"{order}: {order.truck}")
        else:
            print("Receiving location yok")
    """
    print(str(Check_Order_Is_Calculated(56)))

def Check_Order_Is_Calculated(order_id):
    order = Order.objects.get(id= order_id)
    print('order: ',order)
    order_truck_id = order.truck.id
    print('order_truck_id: ',order_truck_id)
    if order_truck_id is None:
        return False
    else:
        return True
    
def Route_Limiter():
    pass

def Calculate_Orders(request):
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
        
    stop_sign = False

    while stop_sign==False:

        if not Order.objects.filter(truck= None).exists():
            messages.success(request, "✅ All orders are assigned to trucks.")
            break

        else:
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
                        truck_number_order = truck.number_of_orders
                        order_in_truck = Order.objects.get(truck__id= truck_id)

                        try:
                            if Route_Limiter(order, order_in_truck, 2):
                                print('Same space route limiter triggered')
                                # To be continued
                        except:
                            pass