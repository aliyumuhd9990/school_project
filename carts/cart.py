from decimal import Decimal
from django.conf import settings
from products.models import Crop


class Cart(object):
    def __init__(self, request):
        """initialize the cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:

            #save an empty cart in the session
            cart = self.session[setting.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, crop, quantity=1, override_quantity=False):
        """Add a crop to the cart or update its quantity"""
        crop_id = str(crop.id)
        if crop_id not in self.cart:
            self.cart[crop_id] = {'quantity':0,
                                  'price': str(crop.crop_price)}
            if override_quantity:
                self.cart[crop_id]['quantity'] = quantity
            else:
                self.cart[crop_id]['quantity'] += quantity
            self.save(self)
        def save(self):
            #mark the session as "modified" to make sure it gets saved
            self.session.modified = True

        def remove(self, crop):
            """Remove a crop from the cart"""
            crop_id = str(crop.id):
            if crop_id in self.cart:
                del self.cart[crop_id]
                self.save()

        def __iter__(self):
            """"iterate over the items in thecart and get the crops from the databas"""
            crop_ids = self.cart.keys()
            #get the crop objects and them to the cart
            crops = Crop.objects.filter(id__in=crop_ids)
            cart = self.cart.copy()
            for crop in crops:
                cart[str(crop.id)]['crop'] = crop
            for item in cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

        def __len__(self):
            """"count all items in the cart"""
            return sum(item['quantity'] for item in self.cart.values())
        
        def get_total_price(self):
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        
        def clear(self):
            del self.session[settings.CART_SESSION_ID]
            self.save()
