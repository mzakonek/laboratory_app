from django.db import models
from laboratory.models import Survey, Parameter
from users.models import User


class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ordered_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"Cart id: {self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='cart_items', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='survey_orders', on_delete=models.CASCADE)

    # parameters are here as ParameterWIthResult table, because we need to assign additional field "result" to it
    parameters = models.ManyToManyField(Parameter, through="ParameterWithResult", related_name='parameter_orders', null=True)

    finished_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'Cart Item id {self.pk} '


class ParameterWithResult(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='parameters_results')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    result = models.CharField(max_length=50, null=True)


