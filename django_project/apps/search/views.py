import random

from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import BaseFormView
from django_filters.views import FilterView

from .forms import ResponseForm
from .models import *
from .utils import PaginateMixin


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialies'] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context['companies'] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        if len(list(Company.objects.annotate(vacancies_count=Count('vacancies')))) >= 8:
            context['companies'] = random.sample(list(Company.objects.annotate(vacancies_count=Count('vacancies'))), 8)
        return context


class VacancyView(ListView):
    model = Vacancy
    queryset = Vacancy.objects.select_related('company')
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 5


class CategoryView(ListView):
    model = Vacancy
    template_name = 'category.html'
    context_object_name = 'vacancies'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__code=self.kwargs['code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialies'] = Specialty.objects.filter(code=self.kwargs['code'])
        return context



    # def get(self, request, code):
    #     specialies = get_object_or_404(Specialty, code=code)
    #     return render(request, 'category.html', context={
    #         'specialies': specialies,
    #         'vacancies': Vacancy.objects.filter(specialty__code=code),
    #     })
    #

class VacancyDetailView(SuccessMessageMixin, BaseFormView, DetailView):
    template_name = 'vacancy.html'
    queryset = Vacancy.objects.select_related('company')
    context_object_name = 'vacancy'
    form_class = ResponseForm
    success_url = 'send/'

    # def get_success_url(self):
    #     return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['already_respond'] = (
            Response.objects.filter(
                vacancy_id=self.kwargs['pk'],
                user_id=self.request.user.pk,
            )
            .exists()
        )
        return context

    def form_valid(self, form):
        application: Response = form.save(commit=False)
        application.vacancy_id = self.kwargs['pk']
        application.user_id = self.request.user.pk
        application.full_clean()
        application.save()
        return super().form_valid(form)


def send_view(request: WSGIRequest, id):
    try:
        vacancies = Vacancy.objects.get(id=id)
    except Vacancy.DoesNotExist:
        raise Http404
    return render(request, 'send.html', context={
        'vacancies': vacancies,
    })