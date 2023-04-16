from django.urls import path, include
from agency_manager import views


app_name = 'agency_manager'
urlpatterns = [
    # Zone
    path('zone/', views.ZoneView.as_view(), name='zone'),
    path('details-zone/<int:id>/', views.DetailsZoneView.as_view(), name="details-zone"),
    path('add-zone/', views.AddZoneView.as_view(), name="zone-add"),
    path('delete-zone/<int:id>/', views.DeleteZoneView.as_view(), name='delete-zone'),
    path('edit-zone/<int:id>/', views.EditZoneView.as_view(), name='edit-zone'),


    # Agence
    path('agence/', views.AgenceView.as_view(), name='agence'),
    path('add-agence/', views.AddAgenceView.as_view(), name="add-agence"),
    path('delete-agence/<int:id>/', views.DeleteAgenceView.as_view(), name='delete-agence'),
    path('edit-agence/<int:id>/', views.EditAgenceView.as_view(), name='edit-agence'),

    # Gestionnaire
    path('gestionnaire/', views.GestionnaireView.as_view(), name='gestionnaire'),
    path('add-gestionnaire/', views.AddGestionnaireView.as_view(), name="add-gestionnaire"),
    path('delete-gestionnaire/<int:id>/', views.DeleteGestionnaireView.as_view(), name='delete-gestionnaire'),
    path('delete-multiple-gestionnaire/', views.DeleteMultipleGestionnaireView.as_view(),
         name='delete-multiple-gestionnaire'),
    path('gestionnaire-details/<int:id>/', views.DetailsGestionnaireView.as_view(),
         name='details-gestionnaire'),
]
