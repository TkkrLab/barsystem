from django.contrib import admin
from .models import Person, Product, Journal

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	list_display = ('id', 'nick_name', 'active', 'member', 'special', 'token', 'first_name', 'last_name', 'amount', 'balance_limit', 'type')
	ordering = ('id',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'special', 'type')
    ordering = ('id',)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
	list_display = ('moment', 'sender', 'recipient', 'product', 'items', 'amount')
	date_hierarchy = 'moment'