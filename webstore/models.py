from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



class StoreCategory(models.Model):
	categoryName = models.CharField(max_length=128)
	def __unicode__(self):
		return unicode(self.categoryName)

class StoreItem(models.Model):
	
	category = models.ForeignKey(StoreCategory)
	itemName = models.CharField(max_length=128)
	itemNameid = models.CharField(max_length=128)
	description = models.CharField(max_length=2048)
	price = models.DecimalField(max_digits=16,decimal_places=2)
	quantity = models.IntegerField(default=0) 
	#picture = models.ImageField(upload_to='store_images', blank=False)
	picture = ProcessedImageField(upload_to='media/store/products',
								processors=[ResizeToFill(250, 185)],
								format='JPEG',
								options={'quality': 60})
	featured_picture = ProcessedImageField(upload_to='media/store/featured',
								processors=[ResizeToFill(800, 300)],
								format='JPEG',
								options={'quality': 60}, blank=True)
	isFeatured = models.BooleanField(default=False)

	canCalcShipping = models.BooleanField(default=False)
	weightPerItem = models.FloatField(default=0)
	numberPerBox = models.IntegerField(default=0)
	boxWidth = models.IntegerField(default=0)
	boxDepth = models.IntegerField(default=0)
	boxHeight = models.IntegerField(default=0)

	isFabric = models.BooleanField(default=False)
	isSmallItem = models.BooleanField(default=False)
	isSwatchKit = models.BooleanField(default=False)
	isFeltingKit = models.BooleanField(default=False)

	def __unicode__(self):
		return  unicode(self.itemName)


class Order(models.Model): # b
	# Many Orders can be related with a single user
	purchaser = models.ForeignKey('user_management.UserProfile', null=True)
	orderDate = models.DateTimeField('Order Date')
	shippingCost = models.DecimalField(max_digits=16,decimal_places=2)
	totalCost = models.DecimalField(max_digits=16,decimal_places=2)
	# need to have total cost be calculated automatically based on the items in the order
	# item = models.ForeignKey(OrderItem)
	# UPS / USPS
	shippingCarrier = models.CharField(max_length=128)
	# overnight, 2 day air, etc
	shippingType = models.CharField(max_length=128)
	#these two are just for amy to help with viewing orders, may integrate into user's current orders on account page eventually
	shippedDate = models.DateTimeField('Shipped Date', null=True)
	deliveredDate = models.DateTimeField('Delivered Date', null=True)
	#shipping vars
	shipToAddress = models.CharField(max_length=128)
	shipToState = models.CharField(max_length=2)
	shipToZipcode = models.CharField(max_length=5)
	def __unicode__(self):
			return  unicode(self.orderDate)
	
class OrderItemCorrect(models.Model):
	itemCost = models.DecimalField(max_digits=16,decimal_places=2)
	itemQuantity = models.IntegerField()
	# Many order Items are related with one order.
	order = models.ForeignKey(Order, null=True) # e
	# Many orderitems can refer to a single store item
	itemID = models.ForeignKey(StoreItem, null=True)
	def __unicode__(self):
			return unicode(self.itemID.itemName)
	def combinedPrice(self):
		return unicode(self.itemCost * self.itemQuantity)
