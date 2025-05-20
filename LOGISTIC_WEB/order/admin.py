from django.contrib import admin
from order.models import Order, Receiving_location, Destination_location, Vehicle, Cargo, Bill, Truck
from order.calculater import testFunc
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render

admin.site.register(Receiving_location)
admin.site.register(Destination_location)
admin.site.register(Vehicle)
admin.site.register(Cargo)
admin.site.register(Bill)
admin.site.register(Truck)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    actions = ["run_testFunc"]

    def run_testFunc(self, request):
        testFunc()
        self.message_user(request, "testFunc() worked", messages.SUCCESS)

        return HttpResponseRedirect(reverse("admin:order_order_changelist"))

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