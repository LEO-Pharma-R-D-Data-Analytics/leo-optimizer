import json
import names
import uuid

from django.core.management.base import BaseCommand

from config.settings import BASE_DIR
from app.models import City
from app.models import Continent
from app.models import Country
from app.models import District
from app.models import Governor
from app.models import Mayor
from app.models import State


class Command(BaseCommand):

    help = 'Seed database'

    def handle(self, *args, **options):
        self.__seed_locations()

    def __seed_locations(self):
        print('Start saving locations.')

        with open(f'{BASE_DIR}/app/management/commands/data/locations.json') as file:
            locations = json.loads(file.read())[:100]
            continent, created = Continent.objects.get_or_create(name='North America')
            country, created = Country.objects.get_or_create(name='USA', continent=continent)

            for location in locations:
                governor, created = Governor.objects.get_or_create(name=str(uuid.uuid4()).split('-')[0])
                state, created = State.objects.get_or_create(name=location['state'], country=country, governor=governor)
                city, created = City.objects.get_or_create(name=location['city'], state=state)
                mayor, created = Mayor.objects.get_or_create(city=city, first_name=names.get_first_name(), last_name=names.get_last_name())
                districts = [District(city=city, name=str(uuid.uuid4()).split('-')[-1]) for _ in range(3)]
                District.objects.bulk_create(districts)

        print('Done saving locations.')
