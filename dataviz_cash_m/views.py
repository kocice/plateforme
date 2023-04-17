# from multiprocessing import context
# from urllib import request
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from json import dumps
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from agency_manager.models import Agence, Gestionnaire, Zone
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from . import utils

data_extractor = utils.Donnees(date='2022-09-22')
data_extractor.getData()


@csrf_exempt
def editDate(request):
    date = request.POST.get('date')
    url = request.POST.get('url')
    global data_extractor
    data_extractor = utils.Donnees(date=date)
    data_extractor.getData()
    return redirect(url)


@login_required(login_url='finlab:login')
def index(request):
    # service = Service.objects.get(name="Cash_M")
    # service = "Cash_M"
    # user = request.user
    # if str(user.service).strip() != service:
    #     raise PermissionDenied

    produit = 'anet'
    dict_portefeuille = data_extractor.getPortefeuille()
    dict_gestionnaire = data_extractor.getInfoGestionnaire(produit=produit)
    dict_non_ab = data_extractor.getNonAbonne(produit=produit)
    dic_direction = data_extractor.directionResumed(produit=produit)
    dic_resum_graph = data_extractor.getResumeGraph(produit=produit)
    dict_info_prod = data_extractor.getInfoProduct(produit=produit)

    evo_produit = data_extractor.evoProduit(produit=produit)
    print(evo_produit)
    data = utils.prodData()
    prod_equipement = utils.getProdEquipement()

    context = {
        'produit': produit,
        'portefeuille': dumps(dict_portefeuille),
        'info_ges': dumps(dict_gestionnaire),
        'info_non_ab': dumps(dict_non_ab),
        'resum_direction': dumps(dic_direction),
        'resum_graph': dumps(dic_resum_graph),
        'info_prod': dumps(dict_info_prod),
        'evo_produit': dumps(evo_produit),
        'data': dumps(data),
        'prod_equipement': dumps(prod_equipement),
    }
    return render(request, "dataviz_cash_m/suivi_produits/home.html", context)


@csrf_exempt
def updateData(request):
    produit = request.POST.get('produit')
    dict_gestionnaire = data_extractor.getInfoGestionnaire(produit=produit)
    dict_non_ab = data_extractor.getNonAbonne(produit=produit)
    dic_direction = data_extractor.directionResumed(produit=produit)
    dic_resum_graph = data_extractor.getResumeGraph(produit=produit)
    dict_info_prod = data_extractor.getInfoProduct(produit=produit)

    evo_produit = data_extractor.evoProduit(produit=produit)

    context = {
        'produit': produit,
        'info_ges': dumps(dict_gestionnaire),
        'info_non_ab': dumps(dict_non_ab),
        'resum_direction': dumps(dic_direction),
        'resum_graph': dumps(dic_resum_graph),
        'info_prod': dumps(dict_info_prod),
        'evo_produit': dumps(evo_produit),
    }
    return JsonResponse(context)

    # @login_required(login_url="auth:login")
    # def synthese(request):
    service = "Cash_M"
    # user = request.user
    # if str(user.service).strip() != service:
    #     raise PermissionDenied

    produit = 'anet'
    evo_produit = data_extractor.evoProduit(produit=produit)
    data = utils.prodData()
    prod_equipement = utils.getProdEquipement()
    context = {
        'evo_produit': dumps(evo_produit),
        'data': dumps(data),
        'prod_equipement': dumps(prod_equipement),
    }
    return render(request, "dataviz_cash_m/suivi_produits/synthese-prod.html", context)


@csrf_exempt
def updateCompaData(request):
    periode = str(request.POST.get('periode'))
    data = utils.prodData(periode)
    context = {
        'data': dumps(data),
    }
    return JsonResponse(context)

    produit = str(request.POST.get('produit'))
    evo_produit = data_extractor.evoProduit(produit=produit)
    context = {
        'evo_produit': dumps(evo_produit),
    }
    return JsonResponse(context)


# class SuiviEquipeView(LoginRequiredMixin, View):
#     def get(self, request):
#         produit = 'anet'
#         greeting = {
#             'pageview': "Dashboards",
#             'products': produit
#         }
#         return render(request, 'dataviz_cash_m/dashbord-dms.html', greeting)
#
#     def post(self, request):
#         # Récupération des données de la requête
#         request_data = json.load(request)
#         date = request_data.get('Date')
#         produit = request.POST.get('produit')
#
#         if univers and product:
#             pass
#
#         elif produit:
#             dict_gestionnaire = data_extractor.getInfoGestionnaire(produit=produit)
#             dict_non_ab = data_extractor.getNonAbonne(produit=produit)
#             dic_direction = data_extractor.directionResumed(produit=produit)
#             dic_resum_graph = data_extractor.getResumeGraph(produit=produit)
#             dict_info_prod = data_extractor.getInfoProduct(produit=produit)
#
#             evo_produit = data_extractor.evoProduit(produit=produit)
#             response_data = {
#                 'produit': produit,
#                 'info_ges': dict_gestionnaire,
#                 'info_non_ab': dict_non_ab,
#                 'resum_direction': dic_direction,
#                 'resum_graph': dic_resum_graph,
#                 'info_prod': dict_info_prod,
#                 'evo_produit': evo_produit,
#             }
#             return JsonResponse(response_data)
#
#         elif univers:
#             instance = data.ManagerSegment(date_debut=start_date, date_fin=end_date, search=search)
#             recap_univers = instance.recapProduit(colonne='univers')
#             top_performers_univers = instance.topPerformer(colonne='univers', choix=univers)
#             response_data = {
#                 'recap_univers': recap_univers,
#                 # 'recap_univers_2': recap_univers_2,
#                 'top_performers_univers': top_performers_univers,
#             }
#             return JsonResponse(response_data)
#
#         else:
#             produit = 'anet'
#             dict_portefeuille = data_extractor.getPortefeuille()
#             dict_gestionnaire = data_extractor.getInfoGestionnaire(produit=produit)
#             dict_non_ab = data_extractor.getNonAbonne(produit=produit)
#             dic_direction = data_extractor.directionResumed(produit=produit)
#             dic_resum_graph = data_extractor.getResumeGraph(produit=produit)
#             dict_info_prod = data_extractor.getInfoProduct(produit=produit)
#
#             evo_produit = data_extractor.evoProduit(produit=produit)
#             data = utils.prodData()
#             prod_equipement = utils.getProdEquipement()
#
#             response_data = {
#                 'produit': produit,
#                 'portefeuille': dumps(dict_portefeuille),
#                 'info_ges': dumps(dict_gestionnaire),
#                 'info_non_ab': dumps(dict_non_ab),
#                 'resum_direction': dumps(dic_direction),
#                 'resum_graph': dumps(dic_resum_graph),
#                 'info_prod': dumps(dict_info_prod),
#                 'evo_produit': dumps(evo_produit),
#                 'data': dumps(data),
#                 'prod_equipement': dumps(prod_equipement),
#             }
#             return JsonResponse(response_data)
