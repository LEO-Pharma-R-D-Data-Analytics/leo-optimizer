import graphene

from app.schema import CityQuery


class Query(CityQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)