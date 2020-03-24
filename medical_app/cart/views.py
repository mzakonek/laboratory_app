from django.conf import settings
from django.contrib import messages

from django.shortcuts import render, redirect
from django.views.generic import DeleteView
from .models import CartItem
from .cart import get_cart_details_context
from django.urls import reverse_lazy


class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = 'cart/cartitem_confirm_delete.html'
    success_url = reverse_lazy('patients:cart_details')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only owner of this CartItem can delete """
        obj = self.get_object()
        try:
            the_id = self.request.session[settings.CART_SESSION_ID]
        except:
            the_id = None
        if not the_id or obj.cart.id != the_id:
            messages.error(request, 'Document not deleted.')
            return redirect('patients:cart_details')
        return super(CartItemDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Survey deleted from your order")
        return super(CartItemDeleteView, self).delete(request, *args, **kwargs)


def cart_details_view(request):
    context = get_cart_details_context(request)
    template = 'cart/detail_view.html'
    return render(request, template, context)