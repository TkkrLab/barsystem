from django.contrib import admin
from django.conf import settings
from .models import Person, Product, ProductTranslation, ProductCategory, Journal, Token
import barsystem_base.functions

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick_name', 'active', 'member', 'special', 'first_name', 'last_name', 'amount', 'balance_limit', 'type')
    ordering = ('id',)

class ProductTranslationInlineAdmin(admin.StackedInline):
    verbose_name = "Translation"
    verbose_name_plural = "Translations"
    model = ProductTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductTranslationInlineAdmin,]
    list_display = ('display_name', 'active', 'special', 'type', 'category', 'member_price_', 'standard_price_')
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
