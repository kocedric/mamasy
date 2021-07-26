from django.contrib import admin
from store.models import *


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'client')
    readonly_fields = ('client', 'gender', 'first_name', 'last_name', 'address', 'phone')


# class AddressInline(admin.StackedInline):
#     model = Address
#     readonly_fields = ('client', 'gender', 'first_name', 'last_name', 'address', 'phone')
#     extra = 1


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('user',)
    # inlines = [
    #     AddressInline,
    # ]


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline
    ]


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    readonly_fields = ('total', 'product', 'qty', 'product_unit_price', 'vat')
    fields = ('product', 'qty', 'product_unit_price', 'vat')
    extra = 3

    def total(self, instance):
        if instance.id:
            return instance.total
        else:
            return ""


class OrderAdmin(admin.ModelAdmin):
    def total(self, instance):
        return instance.total

    list_display = ('order_date', 'client', 'phone', 'shipping_address', 'status', 'total')
    list_filter = ('status', 'shipping_address', 'order_date', 'client')
    readonly_fields = ('order_date', 'client', 'shipping_address', 'total', 'phone')
    inlines = [
        OrderDetailInline,
    ]


admin.site.register(Client, ClientAdmin)
# admin.site.register(Address, AddressAdmin)
admin.site.register(VAT)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
