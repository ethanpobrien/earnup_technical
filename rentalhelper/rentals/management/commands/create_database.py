import codecs
import csv

from django.core.management import BaseCommand
from rentalhelper.rentals.models import Rental
from translation_dictionary import translation_dictionary


class Command(BaseCommand):
    help = 'Management command to backfill rental objects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--filename', help='Specify the CSV to backfill', required=True
        )

    def handle(self, *args, **options):
        filename = options['filename']
        import_data = csv.reader(codecs.open(filename, 'rU', 'utf-8'))
        return backfill_rentals_from_dataset(import_data)


def backfill_rentals_from_dataset(import_data):
    total_created = 0
    for row_count, row_data in enumerate(import_data):
        if row_count == 0:
            continue
        if row_count > 0 and row_count % 1000 == 0:
            print(f'Processed {row_count} rows')
        try:
            data_dict = {
                'ab_id': row_data[0],
                'name': row_data[1],
                'host_id': row_data[2],
                'host_name': row_data[3],
                'neighbourhood_group': row_data[4],
                'neighbourhood': row_data[5],
                'latitude': row_data[6],
                'longitude': row_data[7],
                'room_type': row_data[8],
                'price': row_data[9],
                'minimum_nights': row_data[10],
                'number_of_reviews': row_data[11],
                'last_review': row_data[12],
                'reviews_per_month': row_data[13],
                'calculated_host_listings_count': row_data[14],
                'availability_365': row_data[15],
            }
        except IndexError:
            print('object not created due to index error')
            continue
        try:
            obj, created = Rental.objects.get_or_create(**data_dict)
            if created:
                total_created += 1
        except ValueError:
            print('object not created due to value error')
            continue
        bedroom_count = 0
        for key in translation_dictionary.keys():
            if key in obj.name:
                bedroom_count = translation_dictionary[key]
        if bedroom_count > 0:
            obj.bedroom_count = bedroom_count
            obj.save()

    print(f'Created {total_created} rental objects')
