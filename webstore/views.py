from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from webstore.models import StoreItem, StoreCategory, Order, OrderItemCorrect
from user_management.models import UserProfile
from django.http import HttpResponse
from webstore.bing_search import run_query
import simplejson as json
from haystack.query import SearchQuerySet
from django.forms.models import model_to_dict
from copy import deepcopy
from django.core import serializers
from django.utils import timezone
from django.conf import settings
import requests
import xml.etree.ElementTree as ET
import re

#### need to initialize the cart here so it is accesible initially
def webstore(request,id):
	context = RequestContext(request)    
	#if request.method == 'GET':
	ids = StoreCategory.objects.get(categoryName=id)
	items = StoreItem.objects.filter(category_id=ids.id).all()
	item_categories = StoreCategory.objects.all();

	if not 'cartList' in request.session: # if there is no cart, make one then get its details
		print "making a new cart"
		request.session['cartList'] = []
	initialcart = buildCartDetail(request.session['cartList'])
	subtotal = getSubtotal(initialcart)
	return render_to_response('store/shop-homepage.html', {'initialcart':initialcart, 'subtotal':subtotal, 'items': items, 'item_categories': item_categories},context)

def featured(request):
	
	context = RequestContext(request)
	items = StoreItem.objects.all()
	return render_to_response('index.html',{'success': True, 'items': items}, context)

def home(request):
	context = RequestContext(request)
	return render_to_response('store/shop-homepage.html', {},context )

def searchStore(request):
	context = RequestContext(request)
	
	sqs = SearchQuerySet().filter(content=request.POST.get('search_text'))
	result_list = serializers.serialize('json', StoreItem.objects.filter(itemName__icontains= request.POST.get('search_text') ), fields=('category','itemName','itemNameid','description','price','picture'))
	
	return HttpResponse(result_list, content_type='application/json')

def autocomplete(request):
	sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
	suggestions = [result.itemName for result in sqs]
	# Make sure you return a JSON object, not a bare list.
	# Otherwise, you could be vulnerable to an XSS attack.
	the_data = json.dumps({
		'results': suggestions
	})
	
	return HttpResponse(the_data, content_type='application/json')


def query(request):
	context = RequestContext(request)
	return render_to_response('store/shop-homepage.html',{'success': True},context)

# The car is stored in the session as a dictionary of a dictionary that has
# the primary key of an item and how many were added
def buttonTest(request):
	print "pressed button"
	context = RequestContext(request)
	return render_to_response('store/shop-homepage.html',{'success': True}, context)

def buildCartDetail(sessionCart):
	cartDetails = []
	for itemlist in sessionCart: # sessionCart is a list with elements of [name, quantity]
		item = StoreItem.objects.get(itemNameid = itemlist[0])
		cartDetails.append([item.itemName,item.price,item.quantity,item.quantity * item.price])
	return cartDetails

def getSubtotal(cartDetails):
	sub = 0
	for itemlist in cartDetails:
		sub += itemlist[1]
	return sub

def addToCart(request, itemKey, quantity):
	print "Adding", itemKey, "to cart."
	#print "FLUSHING THE SESSION"
	#request.session.flush()

	context = RequestContext(request)

	if quantity <= 0:
		removeFromCart(request, itemKey)
	if not 'cartList' in request.session:
		print "making a new cart"
		request.session['cartList'] = []
		request.session['cartList'].append([itemKey, quantity])
		# make a new cart
	else:
		print [itemKey, quantity]
		alreadydone = False
		for index in xrange(len(request.session['cartList'])):
			if itemKey == request.session['cartList'][index][0]: # already in list
				print "already in cart, updating quantity"
				request.session['cartList'][index][1] = quantity
				alreadydone = True
				break
		if not alreadydone: # append the new item to the cart
			print "appending to cart"
			request.session['cartList'].append([itemKey, quantity])
		# this works for modifying quantity as well as adding

	request.session.save()
	cart = buildCartDetail(request.session['cartList']) # wondering if this is needed...
	print cart

	sendlist = json.dumps({'cart':cart})
	return HttpResponse(sendlist, content_type='application/json')
	#return render_to_response('store/shop-homepage.html',{'cart':cart,'success': True},context)

def removeFromCart(request, itemKey):
	context = RequestContext(request)
	if 'cartList' in request.session and itemKey in request.session['cartList']:
		pass
		#request.session['cartList'].pop(itemKey)
	request.session.save()
	return render_to_response('store/shop-homepage.html',{'success': True},context)

def deleteCart(request):
	context = RequestContext(request)
	if 'cartList' in request.session:
		request.session.pop('cartList')
	request.session.save()
	return render_to_response('store/shop-homepage.html',{'success': True},context)

# How this works:
# loop through the item names that are in the cart.
# Fetch the matching storeitem
# link that into an orderitem (an order item has a seperate price field and quantity field)
	# that price will just be the same for now. In the future, that might allow
	# for bookstore pricing or promotions to be figured in here.
	# quantity is just how many of the item are being ordered
# link each of those orderitems into a new order object
# save and return that order object to use it for filling in the template
def checkout(request):

	context = RequestContext(request)
	cart = request.session['cartList']
	myOrder = Order() # we have an order object now
	myOrder.orderDate = timezone.now() # date for the order is now
	# these will need to come after probably - I just want to save it
	myOrder.shippingCost = 0
	myOrder.totalCost = 2
	myOrder.save()


	for itemlist in cart: # remember that cart is an array of arrays that have name, quantity, price
		#orderItem = OrderItemCorrect()
		#print "cleaning the order item model"
		# orderItem.full_clean()
		storeItem = StoreItem.objects.get(itemNameid=itemlist[0])
		orderItem = OrderItemCorrect(
			order = myOrder,
			itemID = storeItem,
			itemCost = storeItem.price,
			itemQuantity = int(itemlist[1])
		)
		orderItem.save(force_insert=True)
	
	itemsInOrder = myOrder.orderitemcorrect_set.all()
	
	subtotal = 0
	for items in itemsInOrder:
		subtotal += items.itemCost * items.itemQuantity
	boxDimensions = boxFit(itemsInOrder)
	needToEmail = False
	weight = 0
	if boxDimensions == (0, 0, 0): # determined that it needs to be a manual order
		needToEmail = True 
	else:
		weight = getWeight(itemsInOrder) # calculate weight if it can be shipped
	myOrder.totalCost = subtotal + myOrder.shippingCost # shipping cost is figured out at a later point
	myOrder.save()
	# need to cast as int for stripe to accept it
	cents = int(myOrder.totalCost * 100)
	print cents

	return render_to_response('store/checkout.html',{'weight':weight,'boxW':boxDimensions[0],'boxH':boxDimensions[1],'boxD':boxDimensions[2],'needToEmail':needToEmail,'cents':cents,'order':myOrder, 'items':itemsInOrder, 'success': True},context)

# determine the box size needed
def boxFit(itemsInOrder):
	numSwatchKits = 0
	numFeltingKits = 0
	numSmallItems = 0 # things that could go in a padded mailer
	numFabrics = 0 # if any of these, need to do manual order
	# add up how many of each and return if not shippable.
	for item in itemsInOrder:
		if not item.itemID.canCalcShipping: # items must be marked
			print "Shipping can't be calculated for", item.itemID.itemName 
			return (0,0,0)
		if item.itemID.isFabric: # we'll figure out how to ship fabrics later on
			return (0,0,0)
		elif item.itemID.isSmallItem:
			numSmallItems += item.itemQuantity
		elif item.itemID.isSwatchKit:
			numSwatchKits += item.itemQuantity
		elif item.itemID.isFeltingKit:
			numFeltingKits += item.itemQuantity 
		else: # not marked as anything?
			print "Check to make sure the right fields are marked for", item.itemID.itemName 
			return (0,0,0)
	# now, based on how many of each, determine the right box
	# first check for errors...
	if numFeltingKits > 1:
		print "This order would require more than one box"
		return (0,0,0)
	if numFeltingKits == 1 and numSwatchKits > 0:
		print "This order would require more than one box"
		return (0,0,0)
	if numSwatchKits > 14:
		print "Bulk order, do as an email order"
		return (0,0,0)
	if numSmallItems > 10: # 10 is an abitrary number.
		# just want to make sure they fit in with the rest of the order
		print "Lots of small items, not sure how to handle that"
		return (0,0,0)
	# I think that covers all of the cases we can't do. 
	if numSwatchKits >= 9 or numFeltingKits == 1:
		return (18,12,12)
	if numSwatchKits >= 3:
		return (12,13,9)
	if numSwatchKits == 2:
		return (12,10,5)
	if numSwatchKits == 1:
		return (12,10,3)
	# at this point, the only thing that could be left is an order of just small items
	if numSmallItems > 5:
		return (5, 6, 3) ############ I'm making these up #######################
	if numSmallItems > 0:
		return (4, 5, 2) ############ how to calculate for a bubble mailer? #####
	# if we get here, error


def getWeight(itemsInOrder):
	weight = 0
	for item in itemsInOrder:
		weight += item.itemID.weightPerItem * item.itemQuantity 
	return weight

# function call to submit payment information to Strip
def payment(request):
	context = RequestContext(request)
	
	import stripe
	# Set your secret key: remember to change this to your live secret key in production
	# See your keys here https://manage.stripe.com/account
	stripe.api_key = "sk_test_5LSNQ19L2N0gk7euXWWfWsPO"

	# Get the credit card details submitted by the form
	token = request.POST['stripeToken']
	# Slightly ugly, but functional way of getting value from stripe checkout gui amount_in_cents
    #int(float(request.POST['totalprice']))
	cents = request.POST['totalprice']*100
	stripeEmail = request.POST['stripeEmail']
	try:
        
		charge = stripe.Charge.create(
			amount = cents, # amount in cents, again
			currency = "usd",
			card = token,
			# obtain email from database or from webform?
			description = stripeEmail,
                                      #"payinguser@example.com"
  		)
        
	except stripe.error.CardError, e:
		# Since it's a decline, stripe.error.CardError will be caught
		body = e.json_body
		err  = body['error']

		print "Status is: %s" % e.http_status
		print "Type is: %s" % err['type']
		print "Code is: %s" % err['code']
		# param is '' in this case
		print "Param is: %s" % err['param']
		print "Message is: %s" % err['message']
		
	except stripe.error.InvalidRequestError, e:
		# Invalid parameters were supplied to Stripe's API
		pass
	
	except stripe.error.AuthenticationError, e:
		# Authentication with Stripe's API failed
		# (maybe you changed API keys recently)
		pass
	
	except stripe.error.APIConnectionError, e:
		# Network communication with Stripe failed
		pass
	
	except stripe.error.StripeError, e:
		# Display a very generic error to the user, and maybe send
		# yourself an email
		pass
	
	except Exception, e:
		# Something else happened, completely unrelated to Stripe
		pass
	
	
	request.session.flush()
	#return render_to_response('store/shop-homepage.html',{'success' : True},context)
	#return webstore(request, "Fiber Arts")
	return redirect('webstore', id='Fiber Arts')
# ups
def ups_calculate(request):
    strAccessLicenseNumber = "CCD014DD4CB4AC62"
    strUserId = "jgriner0918"
    strPassword = "From1248"
    strShipperNumber = "R06535"
    strShipperZip = "37167"
    url = "https://www.ups.com/ups.app/xml/Rate"
    strDefaultServiceCode = "03" #Ground Shipping
    shippingtype = request.GET['varShipping']
    if shippingtype == '1DM':
        strDefaultServiceCode = '14'
    elif shippingtype == '1DA':
        strDefaultServiceCode = '01'
    elif shippingtype == '1DP':
        strDefaultServiceCode = '13'
    elif shippingtype == '2DM':
        strDefaultServiceCode = '59'
    elif shippingtype == '2DA':
        strDefaultServiceCode = '02'
    elif shippingtype == '3DS':
        strDefaultServiceCode = '12'
    elif shippingtype == 'GND':
        strDefaultServiceCode = '03'
    
    strDestinationZip = request.GET['varZip']
    weight = "1"
    data = """<?xml version=\"1.0\"?>
        <AccessRequest xml:lang=\"en-US\">
        <AccessLicenseNumber>%s</AccessLicenseNumber>
        <UserId>%s</UserId>
        <Password>%s</Password>
        </AccessRequest>
        <?xml version=\"1.0\"?>
        <RatingServiceSelectionRequest xml:lang=\"en-US\">
        <Request>
        <TransactionReference>
        <CustomerContext>Bare Bones Rate Request</CustomerContext>
        <XpciVersion>1.0001</XpciVersion>
        </TransactionReference>
        <RequestAction>Rate</RequestAction>
        <RequestOption>Rate</RequestOption>
        </Request>
        <PickupType>
        <Code>01</Code>
        </PickupType>
        <Shipment>
        <Shipper>
        <Address>
        <PostalCode>%s</PostalCode>
        <CountryCode>US</CountryCode>
        </Address>
        <ShipperNumber>%s</ShipperNumber>
        </Shipper>
        <ShipTo>
        <Address>
        <PostalCode>%s</PostalCode>
        <CountryCode>US</CountryCode>
        <ResidentialAddressIndicator/>
        </Address>
        </ShipTo>
        <ShipFrom>
        <Address>
        <PostalCode>%s</PostalCode>
        <CountryCode>US</CountryCode>
        </Address>
        </ShipFrom>
        <Service>
        <Code>%s</Code>
        </Service>
        <Package>
        <PackagingType>
        <Code>02</Code>
        </PackagingType>
        <Dimensions>
        <UnitOfMeasurement>
        <Code>IN</Code>
        </UnitOfMeasurement>
        <Length>12</Length>
        <Width>6</Width>
        <Height>36</Height>
        </Dimensions>
        <PackageWeight>
        <UnitOfMeasurement>
        <Code>LBS</Code>
        </UnitOfMeasurement>
        <Weight>%s</Weight>
        </PackageWeight>
        </Package>
        </Shipment>
        </RatingServiceSelectionRequest>
        """ % (strAccessLicenseNumber,strUserId,strPassword,strShipperZip,strShipperNumber,strDestinationZip,strShipperZip,strDefaultServiceCode,weight)
    r = requests.post(url,data)
    rate = ""
    if r.status_code == requests.codes.ok:
        root = ET.fromstring(r.text)
        if root is None:
            rate_value = ""
        else:
            rate = root.find('RatedShipment/TotalCharges/MonetaryValue')
    if rate is None:
        return HttpResponse("")
    else:
        return HttpResponse(rate.text)

def usps_calculate(request):
    userName = "050TEXTI6311"
    orig_zip = "37167"
    varZip = request.GET['varZip']
    varShipping = request.GET['varShipping']#"PRIORITY"#
    if varZip is None:
        return HttpResponse("")
    else:
        result = re.match("^[0-9]{5}(?:-[0-9]{4})?$", varZip)
        if result is None:
            return HttpResponse("InvalidateZip")
        else:
            dest_zip = varZip
    if varShipping is None:
        return HttpResponse("InvalidateShipping")
    else:
        ship = varShipping
    weight = "2"
    url = "http://Production.ShippingAPIs.com/ShippingAPI.dll"
    data = """API=RateV4&XML=
        <RateV4Request USERID=\"%s\">
        <Package ID=\"1ST\">
        <Service>%s</Service>
        <ZipOrigination>%s</ZipOrigination>
        <ZipDestination>%s</ZipDestination>
        <Pounds>%s</Pounds>
        <Ounces>0</Ounces>
        <Container>Variable</Container>
        <Size>REGULAR</Size>
        <Length>18</Length>
        <Height>4</Height>
        <Girth>12</Girth>
        <Machinable>TRUE</Machinable>
        </Package>
        </RateV4Request>""" % (userName,ship,orig_zip,dest_zip,weight)
    r = requests.post(url,data)
    rate = ""
    if r.status_code == requests.codes.ok:
        root = ET.fromstring(r.text)
        if root is None:
            rate_value = ""
        else:
            rate = root.find('Package/Postage/Rate')
    if rate is None:
        return HttpResponse("")
    else:
        return HttpResponse(rate.text)

