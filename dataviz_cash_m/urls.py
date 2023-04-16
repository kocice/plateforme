from django.urls import path
from dataviz_cash_m import views

app_name = 'dms'
urlpatterns = [
    path('dms/', views.index, name='home'),
    path('update-data/', views.updateData, name='update-data'),
    path('synthese-update-compa-data/', views.updateCompaData, name='synthese-update-compa-data'),
    path('edit-date/', views.editDate, name='edit-date'),
]
