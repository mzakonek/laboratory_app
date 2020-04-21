from django import forms
from django.forms.models import inlineformset_factory
from .models import CartItem, ParameterWithResult
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *


class ParameterWithResultForm(forms.ModelForm):

    class Meta:
        model = ParameterWithResult
        exclude = ()



ParameterWithResultFormSet = inlineformset_factory(
    CartItem, ParameterWithResult, form=ParameterWithResultForm,
    fields=('parameter', 'result'), extra=0,
)




class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItem
        exclude = ('cart',)

    def __init__(self, *args, **kwargs):
        super(CartItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('user'),
                Field('survey'),
                Fieldset('Parameters', Formset('formset')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )




# class CartItemForm(forms.ModelForm):
#
#     class Meta:
#         model = CartItem
#         exclude = ('cart',)
#
# TestingFormSet = inlineformset_factory(CartItem, ParameterWithResult, fields=('parameter', 'result'))

