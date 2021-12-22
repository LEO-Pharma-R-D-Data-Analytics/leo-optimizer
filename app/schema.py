import graphene

from graphene_django import DjangoObjectType

from app.models import City
from app.models import Continent
from app.models import Country
from app.models import District
from app.models import Governor
from app.models import Mayor
from app.models import State

from leo_optimizer import gql_optimizer


class ContinentType(DjangoObjectType):

    class Meta:
        model = Continent


class CountryType(DjangoObjectType):

    class Meta:
        model = Country


class StateType(DjangoObjectType):

    class Meta:
        model = State


class DistrictType(DjangoObjectType):

    class Meta:
        model = District


class MayorType(DjangoObjectType):

    class Meta:
        model = Mayor


class CityType(DjangoObjectType):

    class Meta:
        model = City


class GovernorType(DjangoObjectType):

    class Meta:
        model = Governor


class CityQuery(graphene.ObjectType):

    all_cities_optimized = graphene.List(CityType)
    all_cities_not_optimized = graphene.List(CityType)

    def resolve_all_cities_optimized(self, info):
        return gql_optimizer(City.objects.all(), info.field_nodes[0])

    def resolve_all_cities_not_optimized(self, info):
        return City.objects.all()
