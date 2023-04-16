from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from agency_manager import models
from agency_manager import forms
from django.contrib.auth.models import Group
from users.models import CustomUser


# =============================================== Zone =========================================================
class ZoneView(LoginRequiredMixin, View):
    def get(self, request):
        zone_stats = models.Zone.objects.annotate(
            nb_agences=Count('agence', distinct=True),
            nb_gestionnaires=Count('agence__gestionnaire', distinct=True)
        )
        paginator = Paginator(zone_stats, 7)  # Show 7 Users per page.

        context = {
            "zones": paginator.get_page(request.GET.get('page')),
            "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
            "page_title": "Zone"
        }
        return render(request, "agency_manager/administration/zone.html", context)


class EditZoneView(LoginRequiredMixin, View):
    context = {"page_title": "Modification de zone"}

    def get(self, request, id):
        if request.user.has_perm('agency_manager.change_zone'):
            zone_obj = get_object_or_404(models.Zone, id=id)
            form = forms.EditZoneForm(instance=zone_obj)
            self.context["zone_obj"] = zone_obj
            self.context["form"] = form
            return render(request, "agency_manager/administration/zone-add.html", self.context)
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à accéder à cette page !")

    def post(self, request, id):
        zone_obj = get_object_or_404(models.Zone, id=id)
        form = forms.EditZoneForm(request.POST, instance=zone_obj)
        if form.is_valid():
            zone_obj = form.save()
            return redirect('agency_manager:zone')
        else:
            messages.warning(request, 'Quelque a mal fonctionné !')
            self.context['form'] = form
            return render(request, 'agency_manager/administration/zone-add.html', self.context)


class DetailsZoneView(LoginRequiredMixin, View):

    def get(self, request, id):
        if request.user.has_perm('agency_manager.change_zone'):
            zone_obj = get_object_or_404(models.Zone, id=id)
            agence_stats = models.Agence.objects.filter(zone=zone_obj).annotate(
                nb_gestionnaires=Count('gestionnaire', distinct=True)).order_by('agency_name')
            paginator = Paginator(agence_stats, 7)
            print(agence_stats[0].nb_gestionnaires)

            context = {
                "zone_obj": zone_obj,
                "agences": paginator.get_page(request.GET.get('page')),
                "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
                "page_title": "Détail de zone"
            }
            return render(request, "agency_manager/administration/zone-details.html", context)
        else:
            messages.warning("Vous n'êtes autorisé à accéder à cette page")
            raise PermissionDenied()


class AddZoneView(LoginRequiredMixin, View):
    context = {"page_title": "Création de zone"}

    def get(self, request):
        form = forms.ZoneForm()
        self.context['form'] = form
        return render(request, 'agency_manager/administration/zone-add.html', self.context)

    def post(self, request):
        form = forms.ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zone Crée avec Succès')
            return redirect('agency_manager:zone')
        else:
            messages.warning(request, 'Quelque a mal fonctionné !')
            self.context['form'] = form
            return render(request, 'agency_manager/administration/zone-add.html', self.context)


class DeleteZoneView(View):

    def get(self, request, id):
        if request.user.is_authenticated and request.user.has_perm('agency_manager.delete_zone'):
            zone = models.Zone.objects.get(id=id)
            if zone:
                nom_zone = zone.zone_name
                zone.delete()
                messages.success(request, f"Vous venez de supprimer la zone {nom_zone}")
            else:
                messages.warning(request, "Cette zone n'existe pas")
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à supprimer une zone !")
        return redirect('agency_manager:zone')


# =================================================== Agence View ======================================================
class AgenceView(LoginRequiredMixin, View):
    def get(self, request):
        agence_stats = models.Agence.objects.annotate(
            nb_gestionnaires=Count('gestionnaire', distinct=True)
        )
        paginator = Paginator(agence_stats, 7)  # Show 7 Users per page.

        context = {
            "agences": paginator.get_page(request.GET.get('page')),
            "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
            "page_title": "Agence"
        }
        return render(request, "agency_manager/administration/agence.html", context)


class EditAgenceView(LoginRequiredMixin, View):
    context = {"page_title": "Modifier les informations de l'agence"}

    def get(self, request, id):
        if request.user.has_perm('agency_manager.change_agence'):
            agence_obj = get_object_or_404(models.Agence, id=id)
            form = forms.EditAgenceForm(instance=agence_obj)
            self.context["agence_obj"] = agence_obj
            self.context["form"] = form
            print(form)
            return render(request, "agency_manager/administration/add-agence.html", self.context)
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à accéder à cette page !")
            return redirect("agency_manager:agence")

    def post(self, request, id):
        if request.user.has_perm('agency_manager.change_agence'):
            agence_obj = get_object_or_404(models.Agence, id=id)
            form = forms.EditAgenceForm(request.POST, instance=agence_obj)
            if form.is_valid():
                agence_obj = form.save()
                return redirect('agency_manager:agence')
            else:
                messages.warning(request, 'Quelque a mal fonctionné !')
                self.context['form'] = form
                return render(request, 'agency_manager/administration/add-agence.html', self.context)
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à accéder à cette page !")
            return redirect("agency_manager:agence")


class AddAgenceView(LoginRequiredMixin, View):
    context = {"page_title": "Création d'agence"}

    def get(self, request):
        form = forms.AgenceForm()
        self.context['form'] = form
        return render(request, 'agency_manager/administration/add-agence.html', self.context)

    def post(self, request):
        form = forms.AgenceForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agence Crée avec Succès')
            return redirect('agency_manager:agence')
        else:
            messages.warning(request, 'Il existe une agence portant ce nom')
            self.context['form'] = form
            return render(request, 'agency_manager/administration/add-agence.html', self.context)


class DeleteAgenceView(View):

    def get(self, request, id):
        if request.user.is_authenticated and request.user.has_perm('agency_manager.delete_agence'):
            agence = models.Agence.objects.get(id=id)
            if agence:
                nom_agence = agence.agency_name
                agence.delete()
                messages.success(request, f"Vous venez de supprimer l'agence {nom_agence}")
            else:
                messages.warning(request, "Cette agence n'existe pas")
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à supprimer une zone !")
        return redirect('agency_manager:agence')


# ================================================= Gestionnaire View ==================================================
class GestionnaireView(LoginRequiredMixin, View):
    def get(self, request):
        groupe_gestionnaire = Group.objects.get(name="chargé d'affaire")
        gestionnaires_lise = models.Gestionnaire.objects.filter().order_by('id')
        paginator = Paginator(gestionnaires_lise, 7)  # Show 7 Users per page.

        context = {
            "gestionnaires": paginator.get_page(request.GET.get('page')),
            "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
            "page_title": "Gestionnaire"
        }
        return render(request, "agency_manager/administration/gestionnaire.html", context)


class DetailsGestionnaireView(LoginRequiredMixin, View):
    context = None

    def get(self, request, id):
        if request.user.has_perm('agency_manager.view_gestionnaire'):
            gestionnaire_obj = get_object_or_404(models.Gestionnaire, id=id)
            form = forms.EditGestionnaireForm(instance=gestionnaire_obj)
            context = {
                "gestionnaire_obj": gestionnaire_obj,
                "user_group_perms": gestionnaire_obj.gestionnaire.get_group_permissions(),
                "user_perms": gestionnaire_obj.gestionnaire.get_user_permissions(),
                "page_title": "Gestionnaire Details",
                "form": form
            }
            return render(request, "agency_manager/administration/gestionnaire-details.html", context)
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à accéder à cette page !")

    def post(self, request, id):
        gestionnaire_obj = get_object_or_404(models.Gestionnaire, id=id)
        form = forms.EditGestionnaireForm(request.POST, instance=gestionnaire_obj)
        if form.is_valid():
            gestionnaire_obj = form.save()
            return redirect('agency_manager:gestionnaire')
        else:
            messages.warning(request, 'Quelque a mal fonctionné !')
            self.context['form'] = form
            return render(request, 'agency_manager/administration/gestionnaire-details.html', self.context)


class AddGestionnaireView(LoginRequiredMixin, View):
    context = {"page_title": "Créer un Gestionnaire"}

    def get(self, request):
        form = forms.GestionnaireForm()
        self.context['form'] = form
        return render(request, 'agency_manager/administration/add-gestionnaire.html', self.context)

    def post(self, request):
        form = forms.GestionnaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Succès de l'opération")
            return redirect('agency_manager:gestionnaire')
        else:
            messages.warning(request, 'Oops, il semble avoir une erreur')
            self.context['form'] = form
            return render(request, 'agency_manager/administration/add-gestionnaire.html', self.context)


class DeleteGestionnaireView(View):

    def get(self, request, id):
        if request.user.is_authenticated and request.user.has_perm('agency_manager.delete_gestionnaire'):
            gestionnaire = models.Gestionnaire.objects.get(id=id)
            if gestionnaire:
                last_name = gestionnaire.gestionnaire.last_name
                first_name = gestionnaire.gestionnaire.first_name
                gestionnaire.delete()
                messages.success(request, f"Vous venez de supprimer le chargé d'affaire {first_name} {last_name}")
            else:
                messages.warning(request, "Ce chargé d'affaire n'existe pas dans nos bases")
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à supprimer un chargé d'affaire !")
        return redirect('agency_manager:gestionnaire')


class DeleteMultipleGestionnaireView(View):

    def post(self, request):
        if request.user.is_authenticated and request.user.has_perm('agency_manager.delete_gestionnaire'):
            id_list = request.POST.getlist('id[]')
            id_list = [i for i in id_list if i != '']
            for id in id_list:
                user_obj = models.Gestionnaire.objects.get(pk=id)
                if user_obj:
                    user_obj.delete()
                    response = JsonResponse({"success": 'Gestionnaire supprimer avec succès'})
                else:
                    response = JsonResponse({"warning": "Ce gestionnaire n'existe pas"})

            response.status_code = 200
        else:
            messages.warning(request, "Vous n'êtes pas autorisé à supprimer des chargés d'affaires !")
        return response
