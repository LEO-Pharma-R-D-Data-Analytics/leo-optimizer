from django.db import models


class Continent(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class Country(models.Model):
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class Governor(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    governor = models.OneToOneField(Governor, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, related_name='district', on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class Mayor(models.Model):
    city = models.OneToOneField(City, primary_key=True, related_name='mayor', on_delete=models.CASCADE)
    first_name = models.CharField(blank=False, null=False, max_length=32)
    last_name = models.CharField(blank=False, null=False, max_length=32)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
