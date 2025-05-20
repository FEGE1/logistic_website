from django.core.exceptions import ObjectDoesNotExist
from order.models import Order

def testFunc():
    orders = Order.objects.all()
    i=0
    for order in orders:
        if hasattr(order, 'truck'):
            print(f"{order}: {order.truck}")
        else:
            print("Receiving location yok")



"""
def Calculate_Orders():
    orders_by_size=Order_By_Table("orders","size")
    waiting_list=[]

    for order in orders_by_size:
        if order[1] is None:
            waiting_list.append(order)

    stop_sign=False
    while stop_sign==False:

        if not Get_Filter_Table("orders","truck_id","NULL"):
            print("Tüm siparişlere araç atanmıştır !!!")
            break

        else:
            # Space değeri order size değeri ile aynı olan tırları listeye aktarmak için #
            for order in waiting_list:
                order_size = order[5]
                order_id = order[0]
                trucks_ordered_by_space=Order_By_Table("trucks","space")
                trucks_same_space_with_orders = []
                trucks_same_space_with_orders_empty = []
                trucks_bigger_space_with_orders=[]
                trucks_bigger_space_with_orders_empty=[]

                for truck in trucks_ordered_by_space:
                    if order_size == truck[3] and truck[4] < 2:
                        if truck[4] == 1:
                            trucks_same_space_with_orders.append(truck)
                        else:
                            trucks_same_space_with_orders_empty.append(truck)
            # ------------------------------------------------------------------------- #
            # Space değeri order size değerinden yüksek olan ve içinde sipariş olan tırları listeye aktarmak için #
                for truck in trucks_ordered_by_space:
                    if order_size < truck[3] and truck[4] < 2:
                        if truck[4] == 1:
                            trucks_bigger_space_with_orders.append(truck)
                        else:
                            trucks_bigger_space_with_orders_empty.append(truck)
            # ------------------------------------------------------------------------- #
                print(trucks_bigger_space_with_orders)
                # Önceliğimiz tırın tam dolu gitmesi, bu yüzden öncelikle siparişin boyutu ile aynı boş yere sahip olan tırları deneyeceğiz (önce number_of_orders != 0 olan tırlar)
                if trucks_same_space_with_orders:
                    for truck in trucks_same_space_with_orders:
                        print("same space çalıştı")
                        if truck[4] < 2 and not Check_Order_Is_Calculated(order_id): # Şimdilik her tıra maks 2 sipariş atama limiti koydum
                            truck_id = truck[0]
                            truck_number_order = truck[4]
                            order_in_truck = Get_Filter_Table("orders","truck_id",truck_id)[0]

                            try:
                                if Route_Limiter(order,order_in_truck,2): # 2 saatlik (temsili) zaman farkı verdim şimdilik
                                    print("same space route limiter çalıştı")
                                    Update_Value('orders','truck_id',truck_id,"id",order_id)
                                    Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                    Update_Space(order,truck)

                                    stop_sign = True
                            except:
                                print("Hata: Tırdaki sipariş bulunamadı\nTır ID: {}\nİşlemdeki sipariş ID: {}".format(truck_id,order_id))
                    
                    if not Check_Order_Is_Calculated(order_id):
                        continue
                    else:
                        stop_sign = True

                elif trucks_same_space_with_orders_empty:
                    for truck in trucks_same_space_with_orders_empty:
                        if truck[4] < 2 and not Check_Order_Is_Calculated(order_id): # Şimdilik her tıra maks 2 sipariş atama limiti koydum
                            truck_id = truck[0]
                            truck_number_order = truck[4]

                            # Tır komple boş ise direkt ata
                            try:
                                Update_Value('orders','truck_id',truck_id,"id",order_id)
                                Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                Update_Space(order,truck)
                            except:
                                print("Atama işleminde hata")
                    
                    if not Check_Order_Is_Calculated(order_id):
                        continue
                    else:
                        stop_sign=True

                # Hiç bir tırla eşleşme olmadıysa farklı space'e sahip tırları deneyeceğiz
                elif trucks_bigger_space_with_orders:
                    # trucks_bigger_space_with_orders listesini ters çevirip önce daha az yere sahip olan araçları denemesini sağlıyoruz
                    # Bu sayede size' ı 7 olan siparişi, 10 space'i olan yerine 15 space'i olan araca atamasın
                    trucks_bigger_space_with_orders.reverse()
                    for truck in trucks_bigger_space_with_orders:
                        truck_space = truck[3]
                        if truck[4] < 2 and truck_space > order_size and not Check_Order_Is_Calculated(order_id): # Şimdilik her tıra maks 2 sipariş atama limiti koydum
                            truck_id = truck[0]
                            truck_number_order = truck[4]
                            order_in_truck = list(Get_Filter_Table("orders","truck_id",truck_id))[0]

                            try:
                                if Route_Limiter(order,order_in_truck,2): # 2 saatlik (temsili) zaman farkı verdim şimdilik
                                    Update_Value('orders','truck_id',truck_id,"id",order_id)
                                    Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                    Update_Space(order,truck)

                                    stop_sign = True
                            
                            except:
                                print("Hata: Tırdaki sipariş bulunamadı\nTır ID: {}\nİşlemdeki sipariş ID: {}".format(truck_id,order_id))

                    if not Check_Order_Is_Calculated(order_id):
                        continue
                    else:
                        stop_sign=True

                                # BURADA BİR SIKINTI VAR BİGGER_EMPTY OLANLARA DA BAKMASI LAZIM ONU UNUTMUŞUM !!!

                elif trucks_bigger_space_with_orders_empty:

                    trucks_bigger_space_with_orders_empty.reverse()
                    for truck in trucks_bigger_space_with_orders_empty:
                        truck_space = truck[3]
                        if truck[4] == 0 and truck_space > order_size and not Check_Order_Is_Calculated(order_id):
                            truck_id = truck[0]
                            truck_number_order = truck[4]
                            
                            try:
                                Update_Value('orders','truck_id',truck_id,"id",order_id)
                                Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                Update_Space(order,truck)

                                stop_sign = True
                            except:
                                print("Atama işleminde hata")

                    if not Check_Order_Is_Calculated(order_id):
                        continue
                    else:
                        stop_sign=True

                else:
                    print("Genel Hata !!! (Sıkıntı büyük)")
                    stop_sign=True
"""