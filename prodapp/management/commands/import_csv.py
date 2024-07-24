import csv
import os  # Dodaj ten import
from django.core.management.base import BaseCommand
from prodapp.models import Part, Component


class Command(BaseCommand):
    help = 'Load data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Debugging: print the current working directory
        self.stdout.write(f'Current working directory: {os.getcwd()}')

        try:
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')

                # Debugging: print the fieldnames (headers)
                self.stdout.write(f'CSV headers: {reader.fieldnames}')

                # Remove potential whitespace around headers
                reader.fieldnames = [field.strip() for field in reader.fieldnames]

                for row in reader:
                    part_no = row['part_no'].strip()
                    description = row['description'].strip()
                    component_no = row['component_no'].strip()
                    quantity = int(row['quantity'].strip())

                    # Create or get Part
                    part, created = Part.objects.get_or_create(part_no=part_no, defaults={'description': description})

                    # Create or get Component
                    component, created = Component.objects.get_or_create(part=part, component_no=component_no,
                                                                         defaults={'quantity': quantity})

            self.stdout.write(self.style.SUCCESS('Data successfully loaded into the database'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in CSV file: {e}'))