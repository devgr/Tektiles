from django.contrib import admin
from webstore.models import StoreCategory, StoreItem, Order, OrderItemCorrect

class StoreItemAdmin(admin.ModelAdmin):
		fieldsets = (
		(None, { 'fields' : ('category' , 'itemName', 'itemNameid', 'description', 'price','quantity','picture')}),
		('Advanced features', { 'classes' : ('collapse',), 'fields' : ('featured_picture', 'isFeatured', 'canCalcShipping', 'weightPerItem', 'numberPerBox', 'boxWidth', 'boxDepth', 'boxHeight', 'isFabric', 'isSmallItem','isSwatchKit', 'isFeltingKit')}),
		)
		list_display = ('category', 'itemName', 'picture')
		list_display_links = ('category', 'itemName')
		
		
class OrderAdmin(admin.ModelAdmin):
		fieldsets = (
		(None, { 'fields' : ('purchaser' , 'orderDate', 'shippingCarrier','shippingType','shippedDate', 'deliveredDate')}),
		('Advanced features', { 'classes' : ('collapse',), 'fields' : ('shippingCost', 'totalCost', 'shipToAddress', 'shipToState', 'shipToZipcode')}),
		)
		list_display = ('orderDate', 'purchaser', 'shippedDate')
		list_display_links = ('orderDate', 'purchaser', 'shippedDate')

# Register your models here.

admin.site.register(StoreItem, StoreItemAdmin)
admin.site.register(StoreCategory)
admin.site.register(Order, OrderAdmin)
#admin.site.register(OrderItemCorrect)
