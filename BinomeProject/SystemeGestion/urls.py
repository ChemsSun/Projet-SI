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
    path('listeMatierePre/', views.list_matierepremiere,name='list_matierepremiere'),
    path('matirerepr/',views.matierepremiere,name='matierepremiere'),
    path('delete_matierepr/<int:produit_id>/',views.delete_matierepremiere,name='delete_matierepremiere'),
    path('delete_achat/<int:achat_id>/', views.delete_achat, name='delete_achat'),
    path('paiement/<int:fournisseur_id>/',views.reg, name='reg'),
    path('saisir_montant/<int:achat_id>/', views.saisir_montant, name='saisir_montant'),
    path('transfert/',views.creer_transfert),
    path('listeTransfert/',views.fiche_transferts,name='fiche_transferts'),
    path('listeReglements/', views.liste_reglement,name='liste_reglement'),
    path('delete_reglement/<int:reglement_id>/',views.delete_reglement, name='delete_reglement'),
]