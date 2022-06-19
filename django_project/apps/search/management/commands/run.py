from django.core.management.base import BaseCommand

from apps.search.data import specialties, companies, jobs
from apps.search.models import Company, Vacancy, Specialty


class Command(BaseCommand):

    def handle(self, *args, **options):
        Company.objects.all().delete()
        Vacancy.objects.all().delete()
        Specialty.objects.all().delete()

        for special in specialties:
            specialty = Specialty.objects.create(
                code=special['code'],
                title=special['title'],
            )

        for comp in companies:
            company = Company.objects.create(
                id=comp['id'],
                name=comp['title'],
                logo=comp['logo'],
                employee_count=comp['employee_count'],
                description=comp['description'],
                location=comp['location'],
            )

        for job in jobs:
            vacancy = Vacancy.objects.create(
                title_vacancy=job['title'],
                specialty=Specialty.objects.get(code=job['specialty']),
                company=Company.objects.get(id=job['company']),
                salary_min=job['salary_from'],
                salary_max=job['salary_to'],
                published_at=job['posted'],
                skills=job['skills'],
                description=job['description'],
            )
