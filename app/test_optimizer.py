from django.core.management import call_command

from app.client import GraphQLBaseTestCase
from app.models import City
from app.queries import NOT_OPTIMIZED_PAYLOAD
from app.queries import OPTIMIZED_PAYLOAD


class CityTestCase(GraphQLBaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Populate database
        call_command('seed', verbosity=3)

    def setUp(self):
        super().setUp()

    def test_data_exist_query(self):
        cities = City.objects.all()[:10]

        self.assertEqual(len(cities), 10)

    def test_city_not_optimized_query(self):
        r1, q1 = self.query(OPTIMIZED_PAYLOAD, return_queries=True)
        r2, q2 = self.query(NOT_OPTIMIZED_PAYLOAD, return_queries=True)

        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)

        self.assertIsNotNone(r1.json())
        self.assertIsNotNone(r2.json())

        print('Nr. of query after optimization:', len(q1), 'sql queries')
        print('Nr. of query before optimization:', len(q2), 'sql queries')

        # Check that optimization works
        self.assertLess(len(q1), len(q2))
