from django.contrib import admin
from models import *


class ProductInfoInline(admin.TabularInline):
    model = ProductInfo
    extra = 1


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'uName', 'uPwd',
                    'uEmail', 'uPhone', 'uAddr', 'uTime']


class CartListAdmin(admin.ModelAdmin):
    list_display = ['id', 'cPrice', 'cNum', 'cUser', 'cProduct']


class OrderListAdmin(admin.ModelAdmin):
    list_display = ['id', 'oUser', 'oSum', 'oIspay', 'oTime']


class DetailOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'dProduct', 'dNum', 'dPrice', 'dMain']


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pName', 'pPrice', 'pStock',
                    'pDesc', 'pUnit', 'pImg', 'pTime', 'pClass']


class SortAdmin(admin.ModelAdmin):
    list_display = ['id', 'sClass']
    inlines = [ProductInfoInline]
class RencentMapAdmin(admin.ModelAdmin):
    list_display = ['id', 'rUser','rProName','rTime']

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(CartList, CartListAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(DetailOrder, DetailOrderAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(Sort, SortAdmin)
admin.site.register(RencentMap, RencentMapAdmin)
