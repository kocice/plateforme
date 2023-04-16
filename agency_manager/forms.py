from django import forms
from django.db.models import Q

from agency_manager import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


# Création d'une zone
class ZoneForm(forms.ModelForm):
    zone_name = forms.CharField(required=True, label='Nom')
    date_create = forms.CharField(required=False, label='Name', help_text="Example: Can action modelname")
    chef_zone_group = Group.objects.get(name="chef de zone")
    zone_chief = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__in=[chef_zone_group]),
                                        required=True, label="Chef de zone")

    class Meta:
        model = models.Zone
        fields = ['zone_name', 'zone_chief', 'date_create']

    def save(self, commit=True):
        # Save the provided password in hashed format
        zone = super().save()
        return zone


# Modifier une zone
class EditZoneForm(forms.ModelForm):
    zone_name = forms.CharField(required=True, label='Nom')
    chef_zone_group = Group.objects.get(name="chef de zone")
    zone_chief = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__in=[chef_zone_group]),
                                        required=True, label="Chef de zone")

    class Meta:
        model = models.Zone
        fields = ['zone_name', 'zone_chief']

    def save(self, commit=True):
        # Save the provided password in hashed format
        zone = super().save()
        return zone


# Création d'agence
class AgenceForm(forms.ModelForm):
    agency_name = forms.CharField(required=True, label="Nom de l'agence")
    longitude = forms.FloatField(label='Longitude', required=False)
    latitude = forms.FloatField(label='Latitude', required=False)
    date_create = forms.CharField(required=False, label='Name', help_text="Example: Can action modelname")
    chef_agence_group = Group.objects.get(name="chef d'agence")
    agency_manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__in=[chef_agence_group]),
                                            required=True, label="Chef d'agence")
    zone = forms.ModelChoiceField(queryset=models.Zone.objects.all(), required=True, label="Zone")

    class Meta:
        model = models.Agence
        fields = ['agency_name', 'longitude', 'latitude', 'date_create', 'agency_manager', 'zone']

    def save(self, commit=True):
        # Save the provided password in hashed format
        agence = super().save(commit=False)
        agence.zone = self.cleaned_data['zone']
        if commit:
            agence.save()
        return agence


# Modification d'agence
class EditAgenceForm(forms.ModelForm):
    agency_name = forms.CharField(required=True, label="Nom de l'agence")
    longitude = forms.FloatField(label='Longitude', required=False)
    latitude = forms.FloatField(label='Latitude', required=False)
    chef_agence_group = Group.objects.get(name="chef d'agence")
    agency_manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__in=[chef_agence_group]),
                                            required=True, label="Chef d'agence")
    zone = forms.ModelChoiceField(queryset=models.Zone.objects.all(), required=True, label="Zone")

    class Meta:
        model = models.Agence
        fields = ['agency_name', 'longitude', 'latitude', 'agency_manager', 'zone']

    def save(self, commit=True):
        # Save the provided password in hashed format
        agence = super().save(commit=False)
        agence.zone = self.cleaned_data['zone']
        if commit:
            agence.save()
        return agence


# Création d'un chargé d'affaire
class GestionnaireForm(forms.ModelForm):
    gestionnaire_group = Group.objects.get(name="chargé d'affaire")
    gestionnaire = forms.ModelChoiceField(queryset=CustomUser.objects.filter(
        groups__in=[gestionnaire_group]
    ).exclude(
        Q(agence__isnull=False)
    ), required=True, label="Chargé d'affaire")
    agence = forms.ModelChoiceField(queryset=models.Agence.objects.all(), required=True, label="Agence")

    class Meta:
        model = models.Gestionnaire
        fields = ['gestionnaire', 'agence']


# Modifier l'agence associée à un chargé d'affaire
class EditGestionnaireForm(forms.ModelForm):
    agence = forms.ModelChoiceField(queryset=models.Agence.objects.all(), required=True, label="Agence")

    class Meta:
        model = models.Gestionnaire
        fields = ('agence',)
