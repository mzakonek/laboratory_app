from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from cart.cart import get_cart_details_context, update_cart

from ..models import Survey
from ..forms import OrderSurveyWithParameters


class SurveyListView(ListView):
    model = Survey
    template_name = 'laboratory/patients/survey_list.html'
    context_object_name = 'surveys'
    paginate_by = 5


class OrderSurveyWithParams(FormView):
    """
    Create the CartItem with chosen Survey and Parameters; add this CartItem to the Cart
    """

    form_class = OrderSurveyWithParameters
    template_name = 'laboratory/patients/order_survey.html'
    success_url = reverse_lazy('patients:cart_details')

    def get_context_data(self, **kwargs):
        context = super(OrderSurveyWithParams, self).get_context_data(**kwargs)
        context['survey_name'] = get_object_or_404(Survey, pk=self.kwargs.get('pk')).name
        return context

    def get_form_kwargs(self):
        kwargs = super(OrderSurveyWithParams, self).get_form_kwargs()
        survey = get_object_or_404(Survey, pk=self.kwargs.get('pk'))
        kwargs.update({'survey': survey})
        return kwargs

    def form_valid(self, form):
        survey = get_object_or_404(Survey, pk=self.kwargs.get('pk'))
        parameters = form.cleaned_data['available_parameters']

        update_cart(self.request, survey, parameters)

        return super(OrderSurveyWithParams, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Parameters are missing')

        return self.render_to_response(
            self.get_context_data(request=self.request, form=form))

