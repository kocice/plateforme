from django.db import models
from users.models import CustomUser


class Zone(models.Model):
    zone_name = models.CharField(max_length=100, unique=True)
    zone_chief = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.CharField(max_length=150, blank=True, null=True, help_text="Pattern = dd-mm-yyyy")

    def __str__(self):
        return self.zone_name


class Agence(models.Model):
    agency_name = models.CharField(max_length=100, unique=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    agency_manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_create = models.CharField(max_length=150, blank=True, null=True, help_text="Pattern = dd-mm-yyyy")
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.agency_name


class Gestionnaire(models.Model):
    gestionnaire = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gestionnaire.first_name} {self.gestionnaire.last_name}"

