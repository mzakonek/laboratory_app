from django import forms

from .models import Survey, Parameter


class AssignParamsToSurveyForm(forms.ModelForm):
    name = forms.CharField(max_length=15, label='Survey name', disabled=True)
    parameters = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Parameter.objects.all(),
        help_text="Select parameters which should be allowed for Patients when they will be ordering this Survey")

    class Meta:
        model = Survey
        fields = ('name', 'parameters')


class OrderSurveyWithParameters(forms.Form):
    available_parameters = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Parameter.objects.none(),
        help_text="Select the parameters you want to have checked at this Survey")

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')
        super(OrderSurveyWithParameters, self).__init__(*args, **kwargs)
        self.fields['available_parameters'].queryset = survey.parameters.all()


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        fields = ('name',)


ParameterFormSet = forms.modelformset_factory(Parameter, fields=('name',), extra=5, min_num=1)
