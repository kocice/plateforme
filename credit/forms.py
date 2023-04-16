from django import forms
from django.db.models import Q

from credit import models
from credit import models


# Client empruntant
class EmprunteurForm(forms.ModelForm):
    racine = forms.CharField(required=True, label='Racine du compte client')
    nom = forms.CharField(required=True, label='Nom du client')

    class Meta:
        model = models.Emprunteur
        fields = ['racine', 'nom']

    def save(self, commit=True):
        emprunteur = super().save()
        return emprunteur


class LigneCreditForm(forms.ModelForm):
    type_credit = forms.ModelChoiceField(queryset=models.TypeCredit.objects.all(), required=True, label="Type de Crédit")
    montant = forms.IntegerField(required=True, label="Montant de la ligne")
    commentaire = forms.CharField(required=False)

    class Meta:
        model = models.LigneCredit
        fields = ['type_credit', 'montant', 'commentaire']

    def save(self, commit=True):
        # Save the provided password in hashed format
        ligne_credit = super().save()
        return ligne_credit
