from django import forms
from django.forms.models import inlineformset_factory
from .models import CartItem, ParameterWithResult


class ParameterWithResultForm(forms.ModelForm):

    class Meta:
        model = ParameterWithResult
        exclude = ()


class EditParameterWithResultForm(forms.ModelForm):

    class Meta:
        model = ParameterWithResult
        fields = ('parameter', 'result')


EditParameterWithResultFormSet = forms.modelformset_factory(
    ParameterWithResult, fields=('parameter', 'result'), extra=0, form=EditParameterWithResultForm)


ParameterWithResultFormSet = inlineformset_factory(
    CartItem, ParameterWithResult, form=ParameterWithResultForm,
    fields=('parameter', 'result'), extra=0,
)

