
import csv
from django.core.management.base import BaseCommand
from app.models import Country


class Command(BaseCommand):
    help = 'Load countries and risk levels from CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'C:/Users/pauli/PycharmProjects/AAA_draudiklis/app/management/commands/cont.csv'


        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Clear existing data
            Country.objects.all().delete()

            for row in reader:
                Country.objects.create(
                    name=row['Country'],
                    risk_level=row['Risk']
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded country data'))
