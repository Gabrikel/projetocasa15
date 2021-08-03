from django.contrib import admin

from .models import Order

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ['user', 'product', 'paid', 'created', 'modified']
    list_filter = ['paid', 'created', 'modified']
    search_fields = ['user']
    

