from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView
from .models import CartItem, ParameterWithResult
from .cart import get_cart_details_context
from .forms import EditParameterWithResultForm, EditParameterWithResultFormSet
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


class CartItemUpdateView(UpdateView):
    model = ParameterWithResult
    form_class = EditParameterWithResultForm
    template_name = 'cart/cartitem_update_results.html'


    def get_object(self, queryset=None):
        return self.get_cartitem()

    def get_queryset(self):
        return ParameterWithResult.objects.filter(cart_item=self.get_cartitem())

    def get_cartitem(self):
        cartitem_pk = self.kwargs.get('pk')
        return CartItem.objects.get(pk=cartitem_pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = EditParameterWithResultFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return self.form_invalid(request, formset)

    def form_invalid(self, request, formset):
        return render(request, self.template_name, {"formset": formset})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.cart_item = self.get_cartitem()
            instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cart_item'] = self.get_cartitem()
        ctx['formset'] = EditParameterWithResultFormSet(queryset=self.get_queryset())
        return ctx

    def get_success_url(self):
        messages.success(self.request, "Surveys results updated!")
        return reverse_lazy('specialists:orders_items_update', kwargs={'pk': self.kwargs.get('pk')})

