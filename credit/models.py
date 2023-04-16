from django.db import models
from django.db.models import Sum
# from .signals import decision_created_or_updated

from agency_manager.models import Gestionnaire
from users.models import CustomUser


class Emprunteur(models.Model):
    racine = models.CharField(max_length=8, null=True, blank=True)
    nom = models.CharField(max_length=200, null=True, blank=True)
    emprunteur_type = models.CharField(max_length=20, choices=[("client", "Client"), ("prospect", "Prospect")],
                                       default="client")

    def __str__(self):
        return self.id


class TypeCredit(models.Model):
    nom = models.CharField(max_length=200)
    date_ajout = models.DateField(auto_now=True)

    def __str__(self):
        return self.nom


class LigneCredit(models.Model):
    """
    Stocke les informations de base d'une demande de crédit, telles que le nom et les informations de contact
    de l'emprunteur, le montant demandé et la durée souhaitée.
    """
    type_credit = models.ForeignKey(TypeCredit, on_delete=models.SET_NULL, null=True)
    montant = models.IntegerField()
    commentaire = models.TextField(max_length=2000)
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.montant} FCFA"


class Decision(models.Model):
    """
    Stocke les informations de base d'une décision, telles que le statut de la demande de crédit
    (en attente, approuvé, rejeté), ainsi que la date et l'heure de la décision.
    """
    decision = models.CharField(max_length=20, choices=[("approuve", "Approuvé"), ("rejete", "Rejeté")])
    commentaire = models.TextField()
    intervenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_decision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intervenant.first_name} {self.intervenant.last_name} - {self.decision}"


liste_etape = [("gestionnaire", "Chargé d'affaire"), ("chef_agence", "Chef d'agence"),
               ("chef_zone", "Chef de zone"), ("de", "DE"), ("cic", "CIC"),
               ("abi", "ABI"), ("bcp", "BCP")]


class DemandeCredit(models.Model):
    """
    Stoke les informations de crédit demandées à une décision, un intervenant et une demande de crédit.
    Il stocke également les informations d'historique de décision pour chaque demande,
    telles que la date et l'heure de chaque décision, le statut de chaque demande,
    le montant approuvé et d'autres détails pertinents.
    """
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.SET_NULL, null=True)
    chg_initiateur = models.ForeignKey(Gestionnaire, on_delete=models.SET_NULL, null=True)
    ligne_credit = models.ManyToManyField(LigneCredit)
    date_introduction = models.DateTimeField(auto_now_add=True)

    etape = models.CharField(max_length=20, choices=liste_etape, default="gestionnaire")
    decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20,
                              choices=[("en_attente", "En attente"), ("approuve", "Approuvé"), ("rejete", "Rejeté")],
                              default="en_attente")
    commentaire = models.TextField(null=True, blank=True)

    def somme_total_credit(self):
        return LigneCredit.objects.filter(demandecredit=self).aggregate(total=Sum('montant'))['total'] or 0

    def nombre_total_credit(self):
        return LigneCredit.objects.filter(demandecredit=self).count()

    def progression(self):
        if self.etape == "gestionnaire":
            return int((1 / 5) * 100)
        elif self.etape == "chef_agence":
            return int((2 / 5) * 100)
        elif self.etape == "chef_zone":
            return int((3 / 5) * 100)
        elif self.etape == "de":
            return int((4 / 5) * 100)
        else:
            return 100

    def getEtapeNum(self):
        if self.etape == "gestionnaire":
            return 1
        elif self.etape == "chef_agence":
            return 2
        elif self.etape == "chef_zone":
            return 3
        elif self.etape == "de":
            return 4
        else:
            return 5

    def __str__(self):
        return f"{self.ligne_credit} - {self.date_introduction}"


class Notification(models.Model):
    expediteur = models.ForeignKey(CustomUser, related_name='notifications_expediteur', on_delete=models.SET_NULL, null=True)
    destinataire = models.ForeignKey(CustomUser, related_name='notifications_destinataire', on_delete=models.SET_NULL, null=True)
    titre = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    date_envoie = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)
    date_lue = models.DateTimeField(null=True, blank=True, editable=False)
    demande_credit = models.ForeignKey(DemandeCredit, on_delete=models.SET_NULL, null=True)



