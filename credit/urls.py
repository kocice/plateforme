from django.urls import path, include
from credit import views


app_name = 'credit'
urlpatterns = [
    path('credit/', views.CreditView.as_view(), name='credit'),
    path('add-credit/', views.AddCredit.as_view(), name='add-credit'),
    path('api-clients/', views.ClientSearchView.as_view(), name='api-client'),
    path('delete-demande-credit/<int:id>/', views.DeleteDemandeCredit.as_view(), name='delete-credit'),
    path('edit-demande-credit/<int:id>/', views.EditCredit.as_view(), name='edit-credit'),
]
