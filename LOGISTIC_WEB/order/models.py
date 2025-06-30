from django.db import models
from django.utils import timezone
import uuid

class Truck(models.Model):
    plate_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=50)
    size = models.IntegerField()
    space = models.IntegerField()
    number_of_orders = models.IntegerField()

    def __str__(self):
        return f"{self.plate_number} - {self.driver_name}"
    
class Order(models.Model):
    order_code = models.CharField(max_length=10, default=uuid.uuid4, unique=True, editable=False)
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete= models.SET_NULL, null= True, blank= True, related_name="orders")
    status = models.CharField(max_length=30) # Sipariş aktif,pasif,tamamlanmış,iptal...
    price = models.DecimalField(max_digits= 12, decimal_places= 2)
    creation_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"ID: {self.id} - {self.customer.username}"

class Receiving_location(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='receiving_location')
    company_name = models.CharField(max_length=200)
    company_number = models.CharField(max_length=12)
    address = models.TextField()
    pickup_date = models.DateTimeField()

    def __str__(self):
        return f"ID: {self.order.id} - {self.order.customer.username}"

class Destination_location(models.Model): # Durak yerine bu sınıfı kullanacağız
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='destination_location')
    company_name = models.CharField(max_length=200)
    company_number = models.CharField(max_length=12)
    address = models.TextField()
    delivery_date = models.DateTimeField()
   
class Cargo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='cargo')
    type = models.CharField(max_length=30) # elma,armut,tabak taşınacak maddenin ismi /// opsiyonel
    weight = models.IntegerField()
    height = models.IntegerField()
    width =models.IntegerField()
    length = models.IntegerField()
    image = models.ImageField(upload_to='cargo_images',blank=True,null=True)

class Bill(models.Model): # fatura bilgiler
    order = models.OneToOneField(Order,on_delete=models.PROTECT)
    company_name = models.CharField(max_length=200)
    address = models.TextField()
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField()
    satis_vergisi_kimligi = models.CharField(max_length=200)  # Ne olduğunu anlamadım