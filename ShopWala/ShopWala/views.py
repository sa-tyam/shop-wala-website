import pyrebase

from django.shortcuts import render


config = {

	"apiKey": "AIzaSyAL_jkxmrREpofhhEJdepzp_8aMhnXACrA",
    "authDomain": "shopwala-2f42b.firebaseapp.com",
    "databaseURL": "https://shopwala-2f42b.firebaseio.com",
    "projectId": "shopwala-2f42b",
    "storageBucket": "shopwala-2f42b.appspot.com",
    "messagingSenderId": "953563316424",
    "appId": "1:953563316424:web:821a2829891601feb265fd",
    "measurementId": "G-V041QJLZEW"
}

pyre_firebase = pyrebase.initialize_app(config)

pyrebase_auth = pyre_firebase.auth()

pyrebase_database = pyre_firebase.database()

def LandingPage (request):

	request.session.modified = True
	seller_phone = request.GET.get('seller_phone')
	seller_phone = "+" + seller_phone
	request.session['seller_phone'] = str(seller_phone)

	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')

	shop_views =  pyrebase_database.child("Sellers").child(seller_phone).child("StoreViews").child("storeViews").get().val()
	print(shop_views)
	shop_views = int(shop_views)
	print(shop_views)
	shop_views = shop_views + 1
	print(shop_views)
	shop_views_data = {
		"storeViews" : shop_views,
	}
	pyrebase_database.child("Sellers").child(seller_phone).child("StoreViews").set(shop_views_data)

	businessName = pyrebase_database.child("Sellers").child(seller_phone).child("businessName").get().val()
	businessAddress = pyrebase_database.child("Sellers").child(seller_phone).child("businessAddress").get().val()
	ShopImageDownloadUrl = pyrebase_database.child("Sellers").child(seller_phone).child("ShopImageDownloadUrl").get().val()

	return render(request, 'seller_home.html', {"businessName" : businessName,
												"businessAddress" : businessAddress,
												"ShopImageDownloadUrl" : ShopImageDownloadUrl,})

def SignUp (request):

	return render (request, 'signup.html')

def PostSignUp (request):

	phone = request.POST.get('phoneNumber')
	phone = "+91" + phone
	email = request.POST.get('email')
	password = request.POST.get('password')

	try:
		user = pyrebase_auth.create_user_with_email_and_password(email, password)
	except Exception as e:
		message = 'something went wrong'
		return render(request, 'signup.html', {"messg":message})

	data = {
		"phoneNumber" : phone,
	}
	userId = user['localId']
	pyrebase_database.child("Verified-Buyers").child(userId).child("phone").set(data)
	return render(request, 'signin.html')

def SignIn (request):

	return render(request, 'signin.html')

def PostSignIn(request):
	email = request.POST.get('email')
	password = request.POST.get('password')

	try:
		user = pyrebase_auth.sign_in_with_email_and_password(email, password)
	except Exception as e:
		message = 'wrong credentials'
		return render(request, 'signin.html', {"messg":message})
	session_id = user['localId']
	request.session['user_id'] = str(session_id)
	user_mobile = pyrebase_database.child("Verified-Buyers").child(session_id).child("phone").child("phoneNumber").get().val()
	request.session['user_mobile'] = str(user_mobile)
	return render(request, 'seller_home.html')

def PhoneVerify (request):
	return render(request, 'user_phone_form.html')

def PostPhoneVerify (request):
	phoneNumber = request.POST.get('phone-number')
	phoneNumber = "+91"+ phoneNumber
	return render(request, 'user_otp_form.html', {"phoneNumber":phoneNumber})

def UserOtpVerification (request):

	return render (request, 'user_otp_form.html')

def SellerHome (request):
	if not request.session.get('seller_phone', None):
		seller_phone = request.GET.get('seller_phone')
		seller_phone = "+" + seller_phone
		request.session['seller_phone'] = str(seller_phone)
	else:
		seller_phone = request.session['seller_phone']

	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')

	businessName = pyrebase_database.child("Sellers").child(seller_phone).child("businessName").get().val()
	businessAddress = pyrebase_database.child("Sellers").child(seller_phone).child("businessAddress").get().val()
	ShopImageDownloadUrl = pyrebase_database.child("Sellers").child(seller_phone).child("ShopImageDownloadUrl").get().val()

	return render(request, 'seller_home.html', {"businessName" : businessName,
												"businessAddress" : businessAddress,
												"ShopImageDownloadUrl" : ShopImageDownloadUrl,})

def SellerProducts (request):

	phoneNumber = request.session['seller_phone']
	temp_list = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").shallow().get().val()
	print(temp_list)
	product_item_list = []
	product_item_name_list = []
	product_item_description_list = []
	product_item_price_list = []
	product_item_quantityType_list = []
	product_item_productCategory_list = []
	product_item_productId_list = []
	product_item_imageUrl_list = []
	if temp_list:
		for item in temp_list:
			product_item_name = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("name").get().val()
			product_item_name_list.append(product_item_name)
			product_item_description = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("description").get().val()
			product_item_description_list.append(product_item_description)
			product_item_price = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("price").get().val()
			product_item_price_list.append(product_item_price)
			product_item_quantityType = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("quantityType").get().val()
			product_item_quantityType_list.append(product_item_quantityType)
			product_item_productCategory = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productCategory").get().val()
			product_item_productCategory_list.append(product_item_productCategory)
			product_item_productId = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productId").get().val()
			product_item_productId_list.append(product_item_productId)
			product_item_imageUrl = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productImageUrl").get().val()
			product_item_imageUrl_list.append(product_item_imageUrl)

	product_item_list = zip(product_item_name_list, product_item_description_list, product_item_price_list, product_item_quantityType_list, product_item_productCategory_list, product_item_productId_list, product_item_imageUrl_list)

	return render(request, 'seller_products.html', {"product_item_list":product_item_list})

def SellerProductDetails (request):
	phoneNumber = request.session['seller_phone']

	product_views =  pyrebase_database.child("Sellers").child(phoneNumber).child("ProductViews").child("productViews").get().val()
	print(product_views)
	product_views = int(product_views)
	print(product_views)
	product_views = product_views + 1
	print(product_views)
	product_views_data = {
		"productViews" : product_views,
	}
	pyrebase_database.child("Sellers").child(phoneNumber).child("ProductViews").set(product_views_data)

	item = request.GET.get('z')
	product_item_list = []
	product_item_name_list = []
	product_item_description_list = []
	product_item_price_list = []
	product_item_quantityType_list = []
	product_item_productCategory_list = []
	product_item_productId_list = []
	product_item_imageUrl_list = []

	product_item_name = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("name").get().val()
	product_item_name_list.append(product_item_name)
	product_item_description = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("description").get().val()
	product_item_description_list.append(product_item_description)
	product_item_price = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("price").get().val()
	product_item_price_list.append(product_item_price)
	product_item_quantityType = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("quantityType").get().val()
	product_item_quantityType_list.append(product_item_quantityType)
	product_item_productCategory = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productCategory").get().val()
	product_item_productCategory_list.append(product_item_productCategory)
	product_item_productId = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productId").get().val()
	product_item_productId_list.append(product_item_productId)
	product_item_imageUrl = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productImageUrl").get().val()
	product_item_imageUrl_list.append(product_item_imageUrl)

	product_item_list = zip(product_item_name_list, product_item_description_list, product_item_price_list, product_item_quantityType_list, product_item_productCategory_list, product_item_productId_list, product_item_imageUrl_list)

	return render(request, 'seller_product_detail.html', {"product_item_list":product_item_list})

def AddToBag (request):
	if not request.session.get('user_mobile', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		user_mobile = request.session['user_mobile']

	productId = request.GET.get('z')
	print(productId)

	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		print("session found")
		userId = request.session['user_id']
		print(userId)
		data = {"productId": productId}
		if userId:
			pyrebase_database.child("Verified-Buyers").child(userId).child(user_mobile).child("bag").child(productId).push(data)

		return BuyerBag(request)

def BuyNow (request):
	productId = request.GET.get('z')

	phoneNumber = request.session['seller_phone']
	deliveryCharge = pyrebase_database.child("Sellers").child(phoneNumber).child("deliveryCharges").child("deliveryCharge").get().val()
	deliveryFreeOver = pyrebase_database.child("Sellers").child(phoneNumber).child("deliveryCharges").child("deliveryChargeFreeOrder").get().val()

	product_item_name = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(productId).child("name").get().val()
	product_item_quantityType = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(productId).child("quantityType").get().val()
	product_item_imageUrl = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(productId).child("productImageUrl").get().val()


	return render(request, 'buy_now.html', {"productId":productId,
											"product_item_name":product_item_name,
											"product_item_quantityType":product_item_quantityType,
											"product_item_imageUrl":product_item_imageUrl,
											"deliveryCharge":deliveryCharge,
											"deliveryFreeOver":deliveryFreeOver})

def PlaceOrder (request) :

	import time;
	from datetime import datetime, timezone
	import pytz

	tz=pytz.timezone('Asia/Kolkata')

	time_now = datetime.now(tz)
	order_time_now = time_now.strftime('%Y:%m:%d %H:%M')

	phoneNumber = request.session['seller_phone']
	user_mobile = "0"
	if not request.session.get('user_mobile', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		user_mobile = request.session['user_mobile']

	userId = "0"
	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		print("session found")
		userId = request.session['user_id']

	buyerMobile = request.POST.get('mobile')
	buyerMobile = "+91" + buyerMobile
	name = request.POST.get('name')
	itemCount = request.POST.get('itemCount')
	payment = "COD"
	address = request.POST.get('address')
	pinCode = request.POST.get('pinCode')
	buyerCity = request.POST.get('city')

	productId = request.GET.get('z')

	listed_orders = pyrebase_database.child("Orders").child("All").shallow().get().val()
	i = 0
	for item in listed_orders:
		i = i + 1

	orderId = 10000 + i + 1;

	item_count_int = int(itemCount)
	product_item_price = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(productId).child("price").get().val()
	product_item_price = int(product_item_price)

	price = item_count_int * product_item_price
	print(price)

	seller_order_data = {
		"buyerMobile": buyerMobile,
		"itemCount": itemCount,
		"orderId": orderId,
		"orderStatus": "pending",
		"orderTime": order_time_now,
		"payment": payment,
		"price": price,
		"productId": productId,
		"address": address,
		"buyerName" : name,
		"pinCode":pinCode,
		"buyerCity":buyerCity,
	}

	buyer_data = {
		"address": address,
		"name" : name,
		"phoneNumber":buyerMobile,
		"pinCode":pinCode,
	}

	order_order_data = {
		"buyerMobile": buyerMobile,
		"orderId": orderId,
		"productId": productId,
	}

	pending_order_data = {
		"orderId": orderId,
	}


	pyrebase_database.child("Buyers").child(buyerMobile).set(buyer_data)
	pyrebase_database.child("Verified-Buyers").child(userId).child(user_mobile).child("Orders").child(orderId).set(pending_order_data)
	pyrebase_database.child("Orders").child("All").child(orderId).set(order_order_data)
	pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).set(seller_order_data)
	pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("pending").child(orderId).set(pending_order_data)

	pyrebase_database.child("Verified-Buyers").child(userId).child(user_mobile).child("bag").child(orderId).remove()

	return render(request, 'seller_home.html')

def BuyerBag (request):
	phoneNumber = request.session['seller_phone']

	userId = ""
	user_mobile = "0"
	if not request.session.get('user_mobile', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		user_mobile = request.session['user_mobile']

	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		print("session found")
		userId = request.session['user_id']

	bag_items_dict = pyrebase_database.child("Verified-Buyers").child(userId).child(user_mobile).child("bag").shallow().get().val()

	bag_items = []

	if bag_items_dict:
		for item in bag_items_dict:
			bag_items.append(item)
			print(item)
	print(bag_items)

	temp_list = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").shallow().get().val()
	print(temp_list)
	product_item_list = []
	product_item_name_list = []
	product_item_description_list = []
	product_item_price_list = []
	product_item_quantityType_list = []
	product_item_productCategory_list = []
	product_item_productId_list = []
	product_item_imageUrl_list = []
	for item in temp_list:
		product_item_productId = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productId").get().val()
		print(product_item_productId)
		if str(product_item_productId) in bag_items:
			print("yes")
			print(product_item_productId)
			product_item_productId_list.append(product_item_productId)
			product_item_name = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("name").get().val()
			product_item_name_list.append(product_item_name)
			product_item_description = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("description").get().val()
			product_item_description_list.append(product_item_description)
			product_item_price = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("price").get().val()
			product_item_price_list.append(product_item_price)
			product_item_quantityType = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("quantityType").get().val()
			product_item_quantityType_list.append(product_item_quantityType)
			product_item_productCategory = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productCategory").get().val()
			product_item_productCategory_list.append(product_item_productCategory)
			product_item_imageUrl = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(item).child("productImageUrl").get().val()
			product_item_imageUrl_list.append(product_item_imageUrl)


	product_item_list = zip(product_item_name_list, product_item_description_list, product_item_price_list, product_item_quantityType_list, product_item_productCategory_list, product_item_productId_list, product_item_imageUrl_list)

	return render(request, 'buyer_bag.html', {'product_item_list': product_item_list})

def BuyerOrderDetails (request):
	orderId = request.GET.get('z')

	phoneNumber = request.session['seller_phone']
	userId = ""
	user_mobile = "0"
	if not request.session.get('user_mobile', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		user_mobile = request.session['user_mobile']

	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		print("session found")
		userId = request.session['user_id']

	product_item_list = []

	product_buyerMobile_list = []
	product_itemCount_list = []
	product_orderId_list = []
	product_orderStatus_list = []
	product_orderTime_list = []
	product_payment_list = []
	product_price_list = []
	product_productId_list = []
	product_address_list = []
	product_buyerName_list = []
	product_pinCode_list = []
	product_buyerCity_list = []
	product_imageUrl_list = []
	product_item_name_list = []


	product_item_orderId = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("orderId").get().val()
	product_orderId_list.append(product_item_orderId)
	product_buyerMobile = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("buyerMobile").get().val()
	product_buyerMobile_list.append(product_buyerMobile)
	product_itemCount = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("itemCount").get().val()
	product_itemCount_list.append(product_itemCount)
	product_orderStatus = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("orderStatus").get().val()
	product_orderStatus_list.append(product_orderStatus)
	product_orderTime = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("orderTime").get().val()
	product_orderTime_list.append(product_orderTime)
	product_payment = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("payment").get().val()
	product_payment_list.append(product_payment)
	product_price = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("price").get().val()
	product_price_list.append(product_price)
	product_productId = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("productId").get().val()
	product_productId_list.append(product_productId)
	product_address = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("address").get().val()
	product_address_list.append(product_address)
	product_buyerName = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("buyerName").get().val()
	product_buyerName_list.append(product_buyerName)
	product_pinCode = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("pinCode").get().val()
	product_pinCode_list.append(product_pinCode)
	product_buyerCity = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(orderId).child("buyerCity").get().val()
	product_buyerCity_list.append(product_buyerCity)

	product_imageUrl = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(product_productId).child("productImageUrl").get().val()
	product_imageUrl_list.append(product_imageUrl)
	product_item_name = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(product_productId).child("name").get().val()
	product_item_name_list.append(product_item_name)

	product_item_list = zip(product_buyerMobile_list, product_itemCount_list, product_orderId_list, product_orderStatus_list, product_orderTime_list, product_payment_list, product_price_list, product_productId_list, product_address_list, product_buyerName_list, product_pinCode_list, product_buyerCity_list, product_imageUrl_list, product_item_name_list)

	return render(request, 'buyer_order_details.html', {'product_item_list': product_item_list})


def BuyerOrders (request):
	phoneNumber = request.session['seller_phone']
	userId = ""
	user_mobile = "0"
	if not request.session.get('user_mobile', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		user_mobile = request.session['user_mobile']

	if not request.session.get('user_id', None):
		print("session not found")
		return render(request, 'signin.html')
	else:
		print("session found")
		userId = request.session['user_id']

	orders_items_dict = pyrebase_database.child("Verified-Buyers").child(userId).child(user_mobile).child("Orders").shallow().get().val()
	print("order items dict")
	print(orders_items_dict)
	bag_items = []
	if orders_items_dict:
		for item in orders_items_dict:
			bag_items.append(item)
			print("orders")
			print(item)
	print(bag_items)

	temp_list = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").shallow().get().val()
	print(temp_list)

	product_item_list = []

	product_buyerMobile_list = []
	product_itemCount_list = []
	product_orderId_list = []
	product_orderStatus_list = []
	product_orderTime_list = []
	product_payment_list = []
	product_price_list = []
	product_productId_list = []
	product_address_list = []
	product_buyerName_list = []
	product_pinCode_list = []
	product_imageUrl_list = []

	if temp_list:
		for item in temp_list:
			product_item_orderId = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("orderId").get().val()
			print(product_item_orderId)
			if str(product_item_orderId) in bag_items:
				print("yes")
				print(product_item_orderId)
				product_orderId_list.append(product_item_orderId)
				product_buyerMobile = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("buyerMobile").get().val()
				product_buyerMobile_list.append(product_buyerMobile)
				product_itemCount = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("itemCount").get().val()
				product_itemCount_list.append(product_itemCount)
				product_orderStatus = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("orderStatus").get().val()
				product_orderStatus_list.append(product_orderStatus)
				product_orderTime = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("orderTime").get().val()
				product_orderTime_list.append(product_orderTime)
				product_payment = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("payment").get().val()
				product_payment_list.append(product_payment)
				product_price = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("price").get().val()
				product_price_list.append(product_price)
				product_productId = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("productId").get().val()
				product_productId_list.append(product_productId)
				product_address = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("address").get().val()
				product_address_list.append(product_address)
				product_buyerName = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("buyerName").get().val()
				product_buyerName_list.append(product_buyerName)
				product_pinCode = pyrebase_database.child("Sellers").child(phoneNumber).child("orders").child("all").child(item).child("pinCode").get().val()
				product_pinCode_list.append(product_pinCode)
				product_imageUrl = pyrebase_database.child("Sellers").child(phoneNumber).child("Products").child(product_productId).child("productImageUrl").get().val()
				product_imageUrl_list.append(product_imageUrl)

	product_item_list = zip(product_buyerMobile_list, product_itemCount_list, product_orderId_list, product_orderStatus_list, product_orderTime_list, product_payment_list, product_price_list, product_productId_list, product_address_list, product_buyerName_list, product_pinCode_list, product_imageUrl_list)

	return render(request, 'buyer_orders.html', {'product_item_list': product_item_list})
