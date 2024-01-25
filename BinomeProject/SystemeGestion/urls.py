from django.contrib import admin
from django.urls import include, path
from .import views

urlpatterns=[
    path("select2/", include("django_select2.urls")),
    path('',views.home,name='home'),
    path('achat/',views.achat,name='achat'),
    path('listeAchat/',views.liste_achats,name='liste_achats'),
    path('ModiAchat/<int:achat_id>/',views.modifier_achat,name='modifier_achat'),
    path('delete_achat/<int:achat_id>/', views.delete_achat, name='delete_achat'),
    path('saisir_montant/<int:achat_id>/', views.saisir_montant, name='saisir_montant'),
    
    path('fournisseur/',views.fournisseur,name='fournisseur'),
    path('delete_fournisseur/<int:fournisseur_id>/',views.delete_fournisseur,name='delete_fournisseur'),
    path('listeFournisseurs/',views.liste_fournisseurs,name='liste_fournisseurs'),
    path('modiFourni/<int:fournisseur_id>',views.modifier_fournisseur,name='modifier_fournisseur'),
    path('paiement/<int:fournisseur_id>/',views.reg, name='reg'),
    path('listeReglements/', views.liste_reglement,name='liste_reglement'),
    path('delete_reglement/<int:reglement_id>/',views.delete_reglement, name='delete_reglement'),

    path('matirerepr/',views.matierepremiere,name='matierepremiere'),
    path('listeMatierePre/', views.list_matierepremiere,name='list_matierepremiere'),
    path('modifMatiere/<int:produit_id>/',views.modifier_matierepremiere,name='modifier_matierepremiere'),
    path('delete_matierepr/<int:produit_id>/',views.delete_matierepremiere,name='delete_matierepremiere'),

    
    path('creer_transfert/', views.creer_transfert, name='creer_transfert'),
    path('fiche_transferts/', views.fiche_transferts, name='fiche_transfert'),
    path('fiche_transfert_centres/', views.fiche_transfert_centres, name='fiche_transfert_centres'),
    path('centres/<int:centre_id>/fiche_transferts/', views.fiche_transfert_centres, name='fiche_transfert_centres'),

    path('listeCentres/',views.liste_centres,name='liste_centres'),
    path('details_centre/<int:centre_id>/', views.details_centre, name='details_centre'),
    path('centres/<int:centre_id>/employes/', views.employes, name='employes'),
    path('centres/<int:centre_id>/list_employes/', views.list_employes, name='list_employes'),
    path('list_employes/<int:employe_id>/paiment_journalier/', views.paiment_journalier, name='paiment_journalier'),
    path('list_employes/<int:employe_id>/delete_emloyes/', views.delete_emloyes, name='delete_emloyes'),
    path('modifier_employe/<int:employe_id>/', views.modifier_employe, name='modifier_employe'),

    # path('calcul_salaire_mensuel/', views.calculer_salaire_mensuel, name='calcul_salaire_mensuel'),

    path('vente/',views.vendre,name='vente'),
    path('journalvente/',views.journal_vente,name='journal_vente'),
    path('Modivente/<int:vente_id>/',views.modifier_vente,name='modifier_vente'),
    path('suppvente/<int:vente_id>/',views.delete_vente,name='supprimer_vente'),
    
    path('Ajoutcl/',views.client,name='Ajout'),
    path('listecl/',views.listeclient,name='listeclient'),
    path('reglement/<int:vente_id>/', views.reglement, name='reglement'),
    path('liste_reglements/', views.liste_reglements, name='liste_reglements'),
    path('ModiC/<int:client_id>/',views.modifier_client,name='modifier_client'),
    path('suppC/<int:client_id>/',views.supp_client,name='supp_client'),

    path('centres/<int:centre_id>/AjoutP/',views.production,name='AjoutP'),
    path('modifP/<int:product_id>/',views.modifier_product,name='modifP'),
    path('deleteP/<int:product_id>/',views.delete_product,name='deleteP'),
    path('centres/<int:centre_id>/liste_P/', views.list_P, name='listeP'),

    path('centres/<int:centre_id>/AjoutV/',views.ventec,name='AjoutV'),
    path('centres/<int:centre_id>/listeV/', views.list_V, name='listeV'),
    path('modifV/<int:VenteC_id>/',views.modifier_V,name='modifV'),
    path('deleteV/<int:VenteC_id>/',views.delete_V,name='deleteV'),

    path('dashboard/', views.dashboard, name='dashboard'),
]
