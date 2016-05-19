from django.contrib import admin
from .models import Person, Product, ProductCategory, Journal, Token, VendingMachineProduct
import barsystem_base.functions

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick_name', 'active', 'member', 'special', 'first_name', 'last_name', 'amount', 'balance_limit', 'type')
    ordering = ('id',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'special', 'type', 'category', 'member_price_', 'standard_price_')
    ordering = ('id',)

    def member_price_(self, obj):
        return barsystem_base.functions.money_display(obj.member_price)
    def standard_price_(self, obj):
        return barsystem_base.functions.money_display(obj.standard_price)

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('moment', 'sender', 'recipient', 'product', 'items', 'amount')
    date_hierarchy = 'moment'

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('person', 'type', 'value')

@admin.register(VendingMachineProduct)
class VendingMachineProductAdmin(admin.ModelAdmin):
    pass
