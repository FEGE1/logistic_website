from django.contrib import admin
from order.models import Order, Receiving_location, Destination_location, Cargo, Bill, Truck
from order.calculater import testFunc, Calculate_Orders
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render

admin.site.register(Receiving_location)
admin.site.register(Destination_location)
admin.site.register(Cargo)
admin.site.register(Bill)

class ReceivingLocationInLine(admin.StackedInline):
    model = Receiving_location
    can_delete = False
    extra = 0

class DestinationLocationInLine(admin.StackedInline):
    model = Destination_location
    can_delete = False
    extra = 0

class CargoInLine(admin.StackedInline):
    model = Cargo
    can_delete = False
    extra = 0

class TruckInLine(admin.StackedInline):
    model = Truck
    can_delete = False
    extra = 0

class BillInLine(admin.StackedInline):
    model = Bill
    can_delete = False
    extra = 0

class OrderInLine(admin.StackedInline):
    model = Order
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ReceivingLocationInLine, DestinationLocationInLine, CargoInLine, BillInLine]
    actions = ["run_testFunc"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("run-test-func/", self.admin_site.admin_view(self.confirm_test_func_view), name="run_test_func"),
        ]
        return custom_urls + urls


    def changelist_view(self, request, extra_context = None):
        if extra_context is None:
            extra_context = {}

        extra_context['test_func_url'] = 'admin:run_test_func'
        return super().changelist_view(request, extra_context=extra_context)
    
    def confirm_test_func_view(self, request):
        if request.method == "POST":
            testFunc()
            self.message_user(request, "testFunc() başarıyla çalıştırıldı ✔️", messages.SUCCESS)
            return HttpResponseRedirect(reverse("admin:order_order_changelist"))
        
        # GET ile gelindiyse onay sayfasını göster
        return render(request, "admin/order/order/confirm_test_func.html")

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    inlines = [OrderInLine]