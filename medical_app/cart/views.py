from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView
from .models import CartItem
from .cart import get_cart_details_context
from .forms import CartItemForm, ParameterWithResultFormSet  # , TestingFormSet
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


class CartItemUpdate(UpdateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'cart/cartitem_update.html'

    def get_context_data(self, **kwargs):
        data = super(CartItemUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ParameterWithResultFormSet(self.request.POST, instance=self.object)
            data['formset'].full_clean()
        else:
            data['formset'] = ParameterWithResultFormSet(instance=self.object)
        return data

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     print(form)
    #     formset = ParameterWithResultFormSet(self.request.POST, instance=self.object)
    #     if (form.is_valid() and formset.is_valid()):
    #         return self.form_valid(form)
    #
    # def form_invalid(self, form):
    #     pass

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['formset']
        with transaction.atomic():

            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()

        # messages.success(self.request, "The new Parameters were created with success! "
        #                                "Go ahead and assign them to Surveys or create new Parameters!")
        # return render(self.request, self.template_name, {'formset': titles})
        return super(CartItemUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('specialists:orders_list')
