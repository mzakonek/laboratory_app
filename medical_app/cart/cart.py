from django.conf import settings
from .models import Cart, CartItem


def get_cart_details_context(request):
    try:
        the_id = request.session[settings.CART_SESSION_ID]
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        context = {"cart": cart}
    if not the_id or not cart.cart_items.count():
        empty_message = "Your cart is Empty. Order your first survey!"
        context = {"empty": True, "empty_message": empty_message}

    return context


def update_cart(request, survey, parameters):
    print(parameters)

    # get cart id cached in session, if not exist, then create new Cart
    try:
        the_id = request.session[settings.CART_SESSION_ID]
    except:
        new_cart = Cart()
        new_cart.save()
        request.session[settings.CART_SESSION_ID] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    # get CartItem with this Survey and update, or create new CartItem

    cart_item, created = CartItem.objects.get_or_create(cart=cart, survey=survey, user=request.user)
    if created:
        print('cart item created')
    cart_item.parameters.set(parameters, clear=True)




# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#     def add(self, product, quantity=1, update_quantity=False):
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
#         if update_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#         self.save()
#
#     def save(self):
#         self.session[settings.CART_SESSION_ID] = self.cart
#         self.session.modified = True
#
#     def remove(self, product):
#         product_id = str(product.id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()
#
#     def __iter__(self):
#         product_ids = self.cart.keys()
#         products = Product.objects.filter(id__in=product_ids)
#         for product in products:
#             self.cart[str(product.id)]['product'] = product
#
#         for item in self.cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item
#
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
#
#     def clear(self):
#         del self.session[settings.CART_SESSION_ID]
#         self.session.modified = True