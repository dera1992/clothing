from django.contrib import admin
from .models import Order, OrderItem, Address, State, Lga, Payment

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'is_ordered',
                    'paid',
                    'created',
                    'updated',
                   ]
    list_filter = ['paid', 'created', 'updated']

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'state',
        'city',
    ]

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(State)
admin.site.register(Lga)
admin.site.register(Payment)
