from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView
from django.db.models.functions import Now
from django.forms import modelformset_factory, inlineformset_factory
from cart.models import Cart, CartItem, ParameterWithResult
from cart.forms import ParameterWithResultForm, ParameterWithResultFormSet
from django.conf import settings
from .models import Order


def order_checkout(request):
    """Create Order based on the Cart attached to the current session """

    template = 'orders/user_orders_list.html'
    try:
        the_id = request.session[settings.CART_SESSION_ID]
    except:
        return redirect('patients:cart_details')

    cart = Cart.objects.get(id=the_id)
    Order.objects.create(cart=cart, user=request.user)
    cart.ordered_at = Now()

    # delete the Cart ID from the session
    del request.session[settings.CART_SESSION_ID]

    return render(request, template, {})


class UserOrdersListView(ListView):
    """List all orders made by the user"""

    template_name = 'orders/user_orders_list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):

        # get all orders of this user
        orders = self.request.user.orders.all().order_by('-created_at')

        # and all carts attached to those orders
        ordered_carts = [order.cart for order in orders]

        # having all ordered carts, extract CartItems
        ordered_cart_items = []
        for cart in ordered_carts:
            ordered_cart_items.extend(cart.cart_items.all())

        return ordered_cart_items


class OrdersListView(ListView):
    """List all Orders with the Pending status ??"""
    model = Order
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    ordering = ['-status']
    paginate_by = 4


class OrdersDetailView(DetailView):
    model = Order
    template_name = 'orders/orders_detail.html'
    ordering = ['-created_at']



#
# def edit_order_items(request, pk):
#     template_name = 'orders/inlineformset.html'
#     OrderFormSet = inlineformset_factory(CartItem, ParameterWithResult, fields=('parameter', 'result'), extra=3)
#
#     order = get_object_or_404(Order, pk=pk)
#     ordered_cart_items_pks = [i.pk for i in order.cart.cart_items.all()]
#     params_and_results = ParameterWithResult.objects.filter(pk__in=ordered_cart_items_pks)
#
#     formset = OrderFormSet(instance=order.cart.cart_items.all(), queryset=params_and_results)
#     # form = OrderForm(initial={'customer':customer})
#     if request.method == 'POST':
#         print('Printing POST:', request.POST)
#         # form = OrderForm(request.POST)
#         formset = OrderFormSet(request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect('specialists:orders_list')
#
#     context = {'form': formset}
#     return render(request, template_name, context)
#


    #
    # """View for updating all order items at once """
    #
    # template_name = 'orders/order_items_update_formset.html'
    #
    # order = get_object_or_404(Order, pk=pk)
    # ordered_cart_items_pks = [i.pk for i in order.cart.cart_items.all()]
    # params_and_results = ParameterWithResult.objects.filter(pk__in=ordered_cart_items_pks)
    #
    # ProductFormSet = modelformset_factory(ParameterWithResult, fields=('parameter', 'result'), extra=0)
    # data = request.POST or None
    #
    # formset = ProductFormSet(data=data, queryset=params_and_results)
    #
    # if request.method == 'POST' and formset.is_valid():
    #     formset.save()
    #     return redirect('specialists:orders_list')
    #
    # return render(request, template_name, {'formset': formset})
#


class ParameterWithResultsUpdateView(UpdateView):
    model = ParameterWithResult
    template_name = 'orders/order_items_update_formset.html'
    form_class = ParameterWithResult

    def get_context_data(self, **kwargs):
        context = super(ParameterWithResultsUpdateView, self).get_context_data(**kwargs)
        context['formset'] = ParameterWithResultFormset(queryset=Parameter.objects.none())


def edit_order_items(request, pk):
    """View for updating all order items at once """



    """View for updating all order items at once """

    template_name = 'orders/order_items_update_formset.html'

    order = get_object_or_404(Order, pk=pk)
    ordered_cart_items_pks = [i.pk for i in order.cart.cart_items.all()]
    params_and_results = ParameterWithResult.objects.filter(pk__in=ordered_cart_items_pks)
    print(len(params_and_results))

    ProductFormSet = modelformset_factory(ParameterWithResult, fields=('parameter', 'result'), exclude=('parameter',), extra=0)
    data = request.POST or None

    formset = ProductFormSet(data=data, initial=params_and_results)

    if request.method == 'POST' and formset.is_valid():
        formset.save(commit=True)

        return redirect('specialists:orders_list')

    return render(request, template_name, {'formset': formset})


    # # template_name = 'orders/inlineformset.html'
    # template_name = 'orders/order_items_update_formset.html'
    #
    # order = get_object_or_404(Order, pk=pk)
    # ordered_cart_items_pks = [i.pk for i in order.cart.cart_items.all()]
    # params_and_results = ParameterWithResult.objects.filter(pk__in=ordered_cart_items_pks)
    # print(params_and_results)
    #
    # ProductFormSet = modelformset_factory(ParameterWithResult, fields=('parameter', 'result', 'cart_item'), can_delete=False, extra=0)
    # data = request.POST or None
    #
    # # formset = ProductFormSet(data=data, queryset=params_and_results)
    # formset = ProductFormSet(initial=params_and_results)
    #
    # if request.method == 'POST' and formset.is_valid():
    #     formset.data = data
    #     formset.save()
    #     return redirect('specialists:orders_list')
    #
    # return render(request, template_name, {'formset': formset})
