from django.urls import path

from .views import MainView, CategoryView, send_view, VacancyDetailView, VacancyView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/category/<slug:code>/', CategoryView.as_view(), name='category'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy'),
    path('vacancies/', VacancyView.as_view(), name='vacancies'),

    path('vacancies/<int:id>/send/', send_view, name='send'),
]