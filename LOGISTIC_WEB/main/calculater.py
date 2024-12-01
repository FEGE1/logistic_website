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

def Add_Value(table,column,value,id):
    execute0 = "UPDATE {} SET {}={} WHERE id={}".format(table,column,value,id)
    cursor.execute(execute0)
    con.commit()
    
def Calculate_Orders():
    ordered_by_size=Order_By_Table("orders","size")
    waiting_list=[]

    for order in ordered_by_size:
        if order[1] is None:
            waiting_list.append(order)

    while True:
        print("while çalıştı")

        if not Get_Filter_Table("orders","truck_id","NULL"):
            print("Tüm siparişlere araç atanmıştır !!!")
            break
        else:
            for order in waiting_list:
                


    print(waiting_list)
        




            




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
                id=input("Row ID: ")
                column=input("Column name: ")
                value=input("Value: ")
                Add_Value(table,column,value,id)
            except:
                print("Veri Ekleme Başarısız !!!")
    
# Locations = {0,1,2,3,4,5,6,7,8,9,10}