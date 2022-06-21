from django.core.management.base import BaseCommand

from apps.search.data import *
from apps.search.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        Specialty.objects.all().delete()

        for special in specialties:
            specialty = Specialty.objects.create(
                code=special['code'],
                title=special['title'],
            )
