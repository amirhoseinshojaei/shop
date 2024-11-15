
from core.models import Products, Profile

class Cart():
	def __init__(self, request):
		self.session = request.session
		# Get request
		self.request = request
		# Get the current session key if it exists
		cart = self.session.get('session_key')

		# If the user is new, no session key!  Create one!
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}


		# Make sure cart is available on all pages of site
		self.cart = cart

	def db_add(self, product, quantity):
		product_id = str(product)
		product_qty = str(quantity)
		# Logic
		if product_id in self.cart:
			self.cart[product_id]['quantity'] += quantity
		else:
			#self.cart[product_id] = {'price': str(product.price)}
			self.cart[product_id] = int(product_qty)

		self.session.modified = True

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
			current_user.update(old_cart=str(carty))


	def add(self, product, quantity=1):
		product_id = str(product.id)
		product_qty = str(quantity)
		# Logic
		if product_id in self.cart:
			self.cart[product_id]['quantity'] += quantity
		else:
			#self.cart[product_id] = {'price': str(product.price)}
			self.cart[product_id] = int(product_qty)

		self.session.modified = True

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
			current_user.update(old_cart=str(carty))

	def cart_total(self):
		# Get product IDS
		product_ids = self.cart.keys()
		# lookup those keys in our products database model
		products = Products.objects.filter(id__in=product_ids)
		# Get quantities
		quantities = self.cart
		# Start counting at 0
		total = 0
		
		for key, value in quantities.items():
			# Convert key string into into so we can do math
			key = str(key)
			for product in products:
				if str(product.id) == key:
					if product.is_sale:
						total = total + (product.sale_price * value)
					else:
						total = total + (product.price * value)



		return total



	def __len__(self):
		
		return len(self.cart)

	def get_prods(self):
		# Get ids from cart
		product_ids = self.cart.keys()
		# Use ids to lookup products in database model
		products = Products.objects.filter(id__in=product_ids)

		# Return those looked up products
		return products

	def get_quants(self):
		quantities = self.cart
		return quantities

	def update(self, product, quantity):
		product_id = str(product)
		product_qty = int(quantity)

		# Get cart
		ourcart = self.cart
		# Update Dictionary/cart
		ourcart[product_id] = product_qty

		self.session.modified = True
	

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
			current_user.update(old_cart=str(carty))


		thing = self.cart
		return thing

	def delete(self, product):
		product_id = str(product)
		# Delete from dictionary/cart
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
			current_user.update(old_cart=str(carty))

















# from core.models import Products

# class Cart:
#     def __init__(self, request):
#         self.session = request.session

#         # Get the current session key if exist
#         cart = self.session.get('session_key')

#         # If the user is new and no session, Create One
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}

#         # Make sure cart is available all pages
#         self.cart = cart

#     def add(self, product, quantity=1):
#         product_id = str(product.id)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] += quantity
#         else:
#             self.cart[product_id] = {
#                 'quantity': quantity,
#                 'price': str(product.price)
#             }
#         self.save()

#     def save(self):
#         self.session.modified = True

#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())

#     def get_prods(self):
#         # Get ids from cart
#         product_ids = self.cart.keys()
#         # Use id to lookup products in Database model
#         products = Products.objects.filter(id__in=product_ids)
#         # Return those looked up products
#         return products

#     def get_quants(self):
#         quantities = {str(product_id): item['quantity'] for product_id, item in self.cart.items()}
#         return quantities

#     def update(self, product, quantity):
#         product_id = str(product.id)
#         product_qty = str(quantity)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] = product_qty
#         else:
#             self.cart[product_id] = {
#                 'quantity': product_qty,
#                 'price': str(product.price)
#             }
#         self.save()

#     def delete(self, product):
#         product_id = str(product.id)
#         # Delete from dict/cart
#         if product_id in self.cart:
#             del self.cart[product_id]
#         self.save()

#     def cart_total(self):
#         product_ids = self.cart.keys()
#         products = Products.objects.filter(id__in=product_ids)
#         total = 0
#         for product in products:
#             product_id = str(product.id)
#             if product_id in self.cart:
#                 item = self.cart[product_id]
#                 if isinstance(item, dict) and 'quantity' in item:
#                     quantity = item['quantity']
#                     if product.is_sale:
#                         total += product.sale_price * quantity
#                     else:
#                         total += product.price * quantity
#         return total











# from core.models import Products

# class Cart:
#     def __init__(self, request):
#         self.session = request.session

#         # Get the current session key if exist
#         cart = self.session.get('session_key')

#         # If the user is new and no session, Create One
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}

#         # Make sure cart is available all pages
#         self.cart = cart

#     def add(self, product, quantity=1):
#         product_id = str(product.id)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] += quantity
#         else:
#             self.cart[product_id] = {
#                 'quantity': quantity,
#                 'price': str(product.price)
#             }
#         self.save()

#     def save(self):
#         self.session.modified = True

#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())

#     def get_prods(self):
#         # Get ids from cart
#         product_ids = self.cart.keys()
#         # Use id to lookup products in Database model
#         products = Products.objects.filter(id__in=product_ids)
#         # Return those looked up products
#         return products

#     def get_quants(self):
#         return len(self.cart)
#         # quantities = {str(product_id): item['quantity'] for product_id, item in self.cart.items()}
#         # return quantities

#     def update(self, product, quantity):
#         product_id = str(product.id)
#         product_qty = int(quantity)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] = product_qty
#         else:
#             self.cart[product_id] = {
#                 'quantity': product_qty,
#                 'price': str(product.price)
#             }
#         self.save()

#     def delete(self, product):
#         product_id = str(product.id)
#         # Delete from dict/cart
#         if product_id in self.cart:
#             del self.cart[product_id]
#         self.save()

#     def cart_total(self):
#         product_ids = self.cart.keys()
#         products = Products.objects.filter(id__in=product_ids)
#         total = 0
#         for product in products:
#             product_id = str(product.id)
#             if product_id in self.cart:
#                 quantity = self.cart[product_id]['quantity']
#                 if product.is_sale:
#                     total += product.sale_price * quantity
#                 else:
#                     total += product.price * quantity
#         return total



# from core.models import Products

# class Cart:
#     def __init__(self, request):
#         self.session = request.session

#         # Get the current session key if exist
#         cart = self.session.get('session_key')

#         # If the user is new and no session, Create One
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}

#         # Make sure cart is available all pages
#         self.cart = cart

#     def add(self, product, quantity=1):
        
#         product_id = str(product.id)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] += quantity

#         else:
#             self.cart[product_id] = {
#                 'quantity':quantity,
#                 'price':str(product.price)
#             }
        
#         self.save()

#     def save(self):
#         self.session.modified = True


#     def __len__(self):
#         return len(self.cart)
#         # return sum(item['quantity'] for item in self.cart.values())
    
#     def get_prods(self):
#         # Get ids from cart
#         product_ids = self.cart.keys()
#         # Use id to lookup products in Database model
#         product = Products.objects.filter(id__in = product_ids)

#         # Return those lookedup products
#         return product
    

#     def get_quants(self):
#         quantities = self.cart
#         return quantities
    

#     # def update(self, product, quantity):
#     #     product_id = str(product)
#     #     product_qty = int(quantity)

#     #     # Get cart
#     #     ourcart = self.cart
#     #     # Update dictionary/cart
#     #     ourcart[product_id] = product_qty

#     #     self.session.modified = True

#     #     thing = self.cart

#     #     return thing


#     def update(self, product, quantity):
#         product_id = str(product.id)
#         product_qty = int(quantity)

#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] = product_qty

#         else:
#             self.cart[product_id] = {
#                 'quantity':product_qty,
#                 'price':str(product.price)
#             }

#         self.save()

#     def save(self):
#         self.session.modified = True

#     def delete(self, product):
#         product_id = str(product)
#         # Delete from dict/cart
#         if product_id in self.cart:
#             del self.cart['produt_id']

#         self.session.modified = True


#     # def cart_total(self):
#     #     # Get product ids
#     #     product_ids = self.cart.keys()
#     #     # Lookup those keys in our products database
#     #     products = Products.objects.filter(id__in = product_ids)
#     #     # Get quantities
#     #     quantities = self.cart
#     #     # Start counting at 0
#     #     total = 0
#     #     for key, value in quantities.items():
#     #         # key = int(key)
#     #         for product in products:
#     #             # if product.id == key:
#     #             if str(product.id ) == str(key):
#     #                 if product.is_sale:
#     #                     total = total + (product.sale_price * value['quantity'])

#     #                 else:
#     #                     total = total + (product.price * value['quantity'])

#     #         return total


#     def cart_total(self):
#         # Get product ids
#         product_ids = self.cart.keys()
#         # Lookup those keys in our products database
#         products = Products.objects.filter(id__in=product_ids)
#         # Start counting at 0
#         total = 0
#         for product in products:
#             product_id = str(product.id)
#             if product_id in self.cart:
#                 quantity = self.cart[product_id]['quantity']
#                 if product.is_sale:
#                     total += product.sale_price * quantity
#                 else:
#                     total += product.price * quantity
#         return total








# from core.models import Products

# class Cart:
#     def __init__(self, request):
#         self.session = request.session

#         # Get the current session key if exist
#         cart = self.session.get('session_key')

#         # If the user is new and no session, Create One
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}

#         # Make sure cart is available all pages
#         self.cart = cart

#     def add(self, product, quantity=1):
#         product_id = str(product.id)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] += quantity
#         else:
#             self.cart[product_id] = {
#                 'quantity': quantity,
#                 'price': str(product.price)
#             }
#         self.save()

#     def save(self):
#         self.session.modified = True

#     def __len__(self):
#         return len(self.cart)

#     def get_prods(self):
#         # Get ids from cart
#         product_ids = self.cart.keys()
#         # Use id to lookup products in Database model
#         products = Products.objects.filter(id__in=product_ids)
#         # Return those looked up products
#         return products

#     def get_quants(self):
#         quantities = {str(product_id): item['quantity'] for product_id, item in self.cart.items()}
#         return quantities

#     def update(self, product, quantity):
#         product_id = str(product.id)
#         product_qty = int(quantity)
#         if product_id in self.cart:
#             self.cart[product_id]['quantity'] = product_qty
#         else:
#             self.cart[product_id] = {
#                 'quantity': product_qty,
#                 'price': str(product.price)
#             }
#         self.save()

#     def delete(self, product):
#         product_id = str(product.id)
#         # Delete from dict/cart
#         if product_id in self.cart:
#             del self.cart[product_id]  # Corrected from 'produt_id'
#         self.save()

#     def cart_total(self):
#         product_ids = self.cart.keys()
#         products = Products.objects.filter(id__in=product_ids)
#         total = 0
#         for product in products:
#             product_id = str(product.id)
#             if product_id in self.cart:
#                 quantity = self.cart[product_id]['quantity']
#                 if product.is_sale:
#                     total += product.sale_price * quantity
#                 else:
#                     total += product.price * quantity
#         return total
