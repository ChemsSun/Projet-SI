from django.contrib import admin
from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('achat/',views.achat),
    path('fournisseur/',views.fournisseur),
    path('listeAchat/',views.liste_achats,name='liste_achats'),
    path('delete_fournisseur/<int:fournisseur_id>/',views.delete_fournisseur,name='delete_fournisseur'),
    path('listeFournisseurs/',views.liste_fournisseurs,name='liste_fournisseurs'),
]