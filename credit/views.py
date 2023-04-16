import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
import psycopg2
from django.contrib import messages

from datetime import datetime

from agency_manager.models import Agence, Zone, Gestionnaire
from credit import models, forms
from users.models import CustomUser


# =================================================== Credit View ======================================================
def get_user_entities(user):
    # Vérifier si l'utilisateur est chef d'agence
    if Agence.objects.filter(agency_manager=user).exists():
        return 'Agence'

    # Vérifier si l'utilisateur est chef de zone
    if Zone.objects.filter(zone_chief=user).exists():
        return 'Zone'

    # Vérifier si l'utilisateur est gestionnaire
    if Gestionnaire.objects.filter(gestionnaire=user).exists():
        return 'Gestionnaire'

    return None


class CreditView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        context = {
            "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
            "page_title": "Liste de crédit",
        }

        entities = get_user_entities(user)
        if entities == 'Agence':
            agence = Agence.objects.get(agency_manager=user)
            demande_credits = models.DemandeCredit.objects.filter(chg_initiateur__agence=agence)
        elif entities == 'Zone':
            zone = Zone.objects.get(zone_chief=user)
            agences = Agence.objects.filter(zone=zone)  # Récupérer toutes les agences associées à cette zone
            demande_credits = models.DemandeCredit.objects.filter(
                emprunteur__agence__in=agences)  # Filtrer les demandes par les agences de cette zone

        elif entities == 'Gestionnaire':
            gestionnaire = Gestionnaire.objects.get(gestionnaire=user)
            demande_credits = models.DemandeCredit.objects.filter(chg_initiateur=gestionnaire.id)
        else:
            if user.has_perm('credit.view_demande_credit'):
                demande_credits = models.DemandeCredit.objects.all().order_by('-date_introduction')
                context["demande_credits"] = demande_credits
                render(request, "credit/credit.html", context)
            else:
                messages.warning(request, "Vous n'êtes pas autorisé à accéder à cette page")
                return redirect('agency_manager:gestionnaire')

        etape_finale = demande_credits.filter(etape=['cic', 'abi', 'bcp'])

        progression_global = [prog.progression() for prog in demande_credits]
        progression_global = int(sum(progression_global) / len(progression_global))

        context = {
            "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
            "page_title": "Liste de crédit",
            "demande_credits": demande_credits,
            "progression_global": progression_global,
            'entities': entities,
            'etape_gestionnaire': demande_credits.filter(etape='gestionnaire'),
            'etape_chef_agence': demande_credits.filter(etape='chef_agence'),
            'etape_chef_zone': demande_credits.filter(etape='chef_zone'),
            'etape_de': demande_credits.filter(etape='de'),
            'etape_finale': etape_finale,
        }

        return render(request, "credit/credit.html", context)


# =============================================== Credit Client View ===================================================
class AddCredit(LoginRequiredMixin, View):
    context = {
        "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
        "page_title": "Création d'un dossier de crédit",
    }

    def get(self, request):
        form = forms.EmprunteurForm()
        line_form = forms.LigneCreditForm()

        # Récupération de tous les enregistrements de TypeCredit
        types_credit = models.TypeCredit.objects.all()

        # Création de la liste de choix
        choices = [(type_credit.id, type_credit.nom) for type_credit in types_credit]

        self.context['form'] = form
        self.context['line_form'] = line_form
        self.context['choices'] = choices
        return render(request, "credit/add-credit.html", self.context)

    def post(self, request):
        form = forms.EmprunteurForm(request.POST)
        ligne_credit_form = forms.LigneCreditForm(request.POST)

        comment = request.POST.getlist('comment')[0]
        types_credit = request.POST.getlist('type_credit')
        montants = request.POST.getlist('montant')

        try:
            gestionnaire = models.Gestionnaire.objects.get(gestionnaire=request.user.id)
        except models.Gestionnaire.DoesNotExist:
            messages.warning(request, "Seul les chargés d'affaire peuvent monter un dossier de crédit !")
            self.context['form'] = form
            self.context['line_form'] = ligne_credit_form
            return render(request, 'credit/add-credit.html', self.context)
        else:
            if form.is_valid():
                with transaction.atomic():
                    emprunteur_save = form.save()  # Enregistrer et récupérer l'objet LigneCredit enregistré
                    emprunteur = models.Emprunteur.objects.get(id=emprunteur_save.id)

                    if len(montants) == 0 or len(montants) != len(types_credit):
                        messages.warning(request, "Erreur de saisir !")
                    else:
                        lignes_credit = []
                        for i in range(len(types_credit)):
                            type_credit_id = types_credit[i]
                            montant = montants[i]
                            ligne_credit = models.LigneCredit(type_credit_id=type_credit_id, montant=montant)
                            lignes_credit.append(ligne_credit)
                        models.LigneCredit.objects.bulk_create(lignes_credit)

                        demande_credit = models.DemandeCredit.objects.create(
                            emprunteur=emprunteur,
                            chg_initiateur=gestionnaire,
                            commentaire=comment,
                            statut='en_attente',
                        )
                        demande_credit.ligne_credit.add(*lignes_credit)  # utiliser la relation ManyToMany
                        demande_credit.save()

                        notif = models.Notification.objects.create(
                            expediteur=request.user,
                            destinataire=demande_credit.chg_initiateur.agence.agency_manager,
                            titre="En attente d'approbation",
                            message=f"M {request.user} demande votre approbation sur un nouveau dossier de crédit",
                            date_lue=None,
                            demande_credit=demande_credit
                        )
                        notif.save()

                    return redirect('credit:credit')

        messages.error(request, "Erreur lors de l'enregistrement")
        return render(request, 'credit/add-credit.html', self.context)


class EditCredit(LoginRequiredMixin, View):
    def get(self, request, id):
        credit = models.DemandeCredit.objects.get(id=id)
        # lignes_credit = credit.decision.all()
        if credit.decision:
            gestionnaire = Group.objects.get(name="chargé d'affaire")
            decisions_gestionnaire = credit.decision.objects.filter(intervenant__groups=gestionnaire)

        # Récupération de tous les enregistrements de TypeCredit
        types_credit = models.TypeCredit.objects.all()

        # Création de la liste de choix
        choices = [(type_credit.id, type_credit.nom) for type_credit in types_credit]

        context = {'credit': credit, 'choices': choices}
        return render(request, 'credit/credit-edit.html', context)

    def post(self, request, id):
        lignes_credit = models.DemandeCredit.objects.get(id=id).ligne_credit.all()
        data = [
            {
                'id': ligne.id,
                'num_ligne_credit': i + 1,
                'date_demande': datetime.strftime(ligne.date_demande, '%d-%m-%Y %H:%M:%S'),
                'type_credit': str(ligne.type_credit),
                'montant': int(ligne.montant),
                'commentaire': ligne.commentaire
            } for i, ligne in enumerate(lignes_credit)]
        response_data = {
            'data': data
        }
        return JsonResponse(response_data)

    def put(self, request, id):
        r_data = json.loads(request.body)
        ligne_credit = models.DemandeCredit.objects.get(id=id).ligne_credit.get(id=int(r_data['id']))
        # Mettez à jour la ligne de crédit en utilisant les valeurs soumises dans la demande POST
        ligne_credit.type_credit_id = int(r_data['typeCredit'])
        ligne_credit.montant = r_data['montant']
        ligne_credit.commentaire = r_data['commentaire']
        ligne_credit.save()
        return self.post(request, id)

    def delete(self, request, id):
        request_data = json.load(request)
        data_sup = request_data['data']
        ligne_credit_sup = models.DemandeCredit.objects.get(id=id).ligne_credit.get(id=data_sup['id'])
        ligne_credit_sup.delete()
        return self.post(request, id)


class ClientSearchView(View):
    conn = psycopg2.connect(
        dbname='bnk',
        user='postgres',
        password='password',
        host='localhost',
        port='5432'
    )

    def get(self, request):
        search_query = request.GET.get('q')

        request = f"""
            SELECT "ID", "SHORT.NAME", "DESC.ACCOUNT.OFFICER" FROM bnk 
            WHERE CAST("ID" AS TEXT) LIKE '%{search_query}%' LIMIT 20;
        """

        with self.conn.cursor() as cursor:
            cursor.execute(request)
            # cursor.execute(f"""SELECT "ID", "SHORT.NAME", "DESC.ACCOUNT.OFFICER" FROM bnk""")
            clients = cursor.fetchall()

        response_data = {'clients': clients}
        # return render(request, "credit/add-credit.html", context)
        return JsonResponse(response_data)


class DeleteDemandeCredit(LoginRequiredMixin, View):
    def get(self, request, id):
        demande_credit = get_object_or_404(models.DemandeCredit, id=id)

        demande_credit.delete()
        return redirect('credit:credit')
