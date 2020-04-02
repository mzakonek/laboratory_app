from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView


from ..models import Survey, Parameter
from ..forms import AssignParamsToSurveyForm, ParameterFormSet, ParameterForm


class SurveyCreateView(CreateView):
    model = Survey
    fields = ('name', 'description', )
    template_name = 'laboratory/specialists/add_form.html'

    def form_valid(self, form):
        survey = form.save(commit=False)
        survey.owner = self.request.user
        survey.save()
        messages.success(self.request, 'The survey was created with success! Go ahead and add parameters now.')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super(SurveyCreateView, self).get_context_data(**kwargs)
        context['type_to_add'] = "Survey"
        return context


class SurveyListView(ListView):
    model = Survey
    template_name = 'laboratory/specialists/list_view.html'
    context_object_name = 'surveys'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        context['list_type_header'] = "All Surveys"
        return context


class SurveyDeleteView(DeleteView):
    model = Survey
    template_name = 'laboratory/specialists/survey_confirm_delete.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            messages.error(request, 'You are not allowed to delete this Survey.')
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)


class ParameterCreateView(CreateView):
    model = Parameter
    template_name = 'laboratory/specialists/add_formset.html'
    form_class = ParameterForm

    def get_context_data(self, **kwargs):
        context = super(ParameterCreateView, self).get_context_data(**kwargs)
        context['formset'] = ParameterFormSet(queryset=Parameter.objects.none())
        context['type_to_add'] = 'Parameters'
        return context

    def post(self, request, *args, **kwargs):
        formset = ParameterFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return render(request, self.template_name, {'formset': formset})

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        messages.success(self.request, "The new Parameters were created with success! "
                                       "Go ahead and assign them to Surveys or create new Parameters!")
        return redirect('specialists:parameter_add')


class AssignParamsToSurveyView(UpdateView):
    model = Survey
    form_class = AssignParamsToSurveyForm
    template_name = 'laboratory/specialists/update_view.html'

    def form_valid(self, form):
        params = form.cleaned_data['parameters']
        survey = form.save(commit=False)
        survey.parameters.add(*params)
        survey.save()
        messages.success(self.request, "You have just updated parameters assigned to the survey!")
        return redirect('specialists:survey_update', survey.pk)

    def get_context_data(self, **kwargs):
        context = super(AssignParamsToSurveyView, self).get_context_data(**kwargs)
        context['type_to_add'] = "Parameters to the Survey"
        return context