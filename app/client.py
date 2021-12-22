from django.db import connection
from django.test.utils import CaptureQueriesContext
from graphene_django.utils.testing import GraphQLTestCase


class GraphQLBaseTestCase(GraphQLTestCase):

    GRAPHQL_SCHEMA = 'config.schema.schema'

    def setUp(self):
        super().setUp()

    def query(self, query, operation_name=None, input_data=None, variables=None, headers=None, return_queries=False):
        if headers is None:
            headers = {}

        if "secure" not in headers:
            headers = {"secure": True}

        if not return_queries:
            return super().query(query, operation_name=operation_name, input_data=input_data, variables=variables, headers=headers)

        with CaptureQueriesContext(connection) as ctx:
            response = super().query(query, operation_name=operation_name, input_data=input_data, variables=variables, headers=headers)

            return response, ctx.captured_queries
