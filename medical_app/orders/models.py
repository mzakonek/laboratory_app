from django.db import models
from users.models import User
from cart.models import Cart

STATUS_CHOICES = (
    ("P", "Processed"),
    ("F", "Finished"),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")

    def __str__(self):
        return f'Order ID: {self.pk} ordered by userID:{self.user.pk}'

    def get_number_of_surveys(self):
        return self.cart.cart_items.count()
