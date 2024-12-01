from calculater_model import order
import sqlite3

# SQL CONNECTION

con = sqlite3.connect("ORDER_TEST.db")
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS trucks (truck_id INTEGER PRIMARY KEY,name TEXT,size INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY,truck_id INTEGER,status TEXT,receiving_loc TEXT,destination_loc TEXT, FOREIGN KEY (truck_id) REFERENCES trucks (truck_id))")

# FUNC SECTİON

def Create_Order(status,receiving,destination):
    execute0 = "INSERT INTO orders (status,receiving_loc,destination_loc) VALUES('{}','{}','{}')".format(status,receiving,destination)
    cursor.execute(execute0)
    con.commit()

def Delete_Order(id):
    execute0 = "DELETE FROM orders WHERE id = {}".format(id)
    cursor.execute(execute0)
    con.commit()

def Get_Table(table):
    execute0 = "SELECT * FROM {}".format(table)
    Table_List=list(cursor.execute(execute0))
    return Table_List

def Get_Filter_Table(table,filter,value):
    if value == "NULL":
        execute0 = "SELECT * FROM {} WHERE {} is NULL".format(table,filter)
        Table_List=list(cursor.execute(execute0))
        return Table_List
    else:
        execute0 = "SELECT * FROM {} WHERE {}={}".format(table,filter,value)
        Table_List=list(cursor.execute(execute0))
        return Table_List

def Order_By_Table(table,column):
    execute0 = "SELECT * FROM {} ORDER BY {} DESC".format(table,column)
    order_by_size=cursor.execute(execute0)
    return order_by_size

def Update_Value(table,column,value,id_column_name,id):
    execute0 = "UPDATE {} SET {}={} WHERE {}={}".format(table,column,value,id_column_name,id)
    print(execute0)
    cursor.execute(execute0)
    con.commit()

def Update_Space(order,truck):
    order_size=order[5]
    truck_id=truck[0]
    truck_space=truck[3]
    update_space= truck_space - order_size

    Update_Value("trucks","space",update_space,"truck_id",truck_id)

def Route_Limiter(x,y,time_limit):
    x_receiving=int(x[3])
    x_destination=int(x[4])
    y_receiving=int(y[3])
    y_destination=int(y[4])
    print(x)
    print(y)

    total_time_dif = (abs(x_receiving-y_receiving))+(abs(x_destination-y_destination))
    print(total_time_dif)

    if total_time_dif <= time_limit:
        return True
    else:
        return False

def Calculate_Orders():
    orders_by_size=Order_By_Table("orders","size")
    waiting_list=[]

    for order in orders_by_size:
        if order[1] is None:
            waiting_list.append(order)

    while True:
        print("while çalıştı")

        if not Get_Filter_Table("orders","truck_id","NULL"):
            print("Tüm siparişlere araç atanmıştır !!!")
            break

        else:
            for order in waiting_list:
                order_size = order[5]
                order_id = order[0]
                trucks_ordered_by_space=Order_By_Table("trucks","space")
                trucks_same_space_with_orders = []
                trucks_same_space_with_orders_empty = []

                for truck in trucks_ordered_by_space:
                    if order_size == truck[3] and truck[4] < 2:
                        if truck[4] == 1:
                            trucks_same_space_with_orders.append(truck)
                        else:
                            trucks_same_space_with_orders_empty.append(truck)

                # Önceliğimiz tırın tam dolu gitmesi, bu yüzden öncelikle siparişin boyutu ile aynı boş yere sahip olan tırları deneyeceğiz
                if trucks_same_space_with_orders:
                    for truck in trucks_same_space_with_orders:
                        if truck[4] < 2: # Şimdilik her tıra maks 2 sipariş atama limiti koydum
                            truck_id = truck[0]
                            truck_number_order = truck[4]
                            order_in_truck = Get_Filter_Table("orders","truck_id",truck_id)

                            # Tır komple boş ise direkt ata
                            try:
                                if Route_Limiter(order,order_in_truck[0],2): # 2 saatlik (temsili) zaman farkı verdim şimdilik
                                    Update_Value('orders','truck_id',truck_id,"id",order_id)
                                    Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                    Update_Space(order,truck)
                            except:
                                print("Hata kodu 001")
                        

                elif trucks_same_space_with_orders_empty:
                    for truck in trucks_same_space_with_orders_empty:
                        if truck[4] < 2: # Şimdilik her tıra maks 2 sipariş atama limiti koydum
                            truck_id = truck[0]
                            truck_number_order = truck[4]
                            order_in_truck = Get_Filter_Table("orders","truck_id",truck_id)

                            # Tır komple boş ise direkt ata
                            if not order_in_truck:
                                Update_Value('orders','truck_id',truck_id,"id",order_id)
                                Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                Update_Space(order,truck)

                # Hiç bir tırla eşleşme olmadıysa farklı space'e sahip tırları deneyeceğiz
                else:
                    for truck in trucks_ordered_by_space:
                        truck_space = truck[3]
                        if truck[4] < 2 and truck_space > order_size: # Şimdilik her tıra maks 2 sipariş atama limiti koydum
                            truck_id = truck[0]
                            truck_number_order = truck[4]
                            order_in_truck = list(Get_Filter_Table("orders","truck_id",truck_id))[0]

                            if not order_in_truck:
                                Update_Value('orders','truck_id',truck_id,"id",order_id)
                                Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                Update_Space(order,truck)
                                
                            else:
                                if Route_Limiter(order,order_in_truck,2): # 2 saatlik (temsili) zaman farkı verdim şimdilik
                                    Update_Value('orders','truck_id',truck_id,"id",order_id)
                                    Update_Value('trucks','number_of_orders',(truck_number_order+1),'truck_id',truck_id)
                                    Update_Space(order,truck)

# MAIN SECTION

while True:
    print("*******************************")
    print("1- Create New Order")
    print("2- Delete Order")
    print("3- Calculate")
    print("4- Get Table")
    print("5- Get Table With Filter")
    print("6- Add Value to Row")
    print("q- Quit")

    operation = str(input("Select: ")).lower()

    if operation == "q":
        break
    else:
        if operation == "1":
            status = input("Order Status: ")
            receiving = str(input("Receiving Location: "))
            destination = str(input("Destination Location: "))

            Create_Order(status,receiving,destination)

        elif operation == "2":
            id = input("Order id: ")
            execute0 = "SELECT * FROM orders WHERE id = {}".format(id)
            f_order = cursor.execute(execute0).fetchone()
            print(f_order) 
            Delete_Order(id)
        
        elif operation == "3":
            Calculate_Orders()
        elif operation == "4":
            table=input("Table name: ")
            print(Get_Table(table))
        elif operation == "5":
            table=input("Table name: ")
            filter=input("Column name: ")
            value=input("Value : ")
            print(Get_Filter_Table(table,filter,value))
        elif operation == "6":
            try:
                table=input("Table name: ")
                id_column_name=input("Id column name: ")
                id=input("Row ID: ")
                column=input("Column name: ")
                value=input("Value: ")
                Update_Value(table,column,value,id_column_name,id)
            except:
                print("Veri Ekleme Başarısız !!!")
    
# Locations = {0,1,2,3,4,5,6,7,8,9,10}