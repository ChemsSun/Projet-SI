from django.contrib import admin
from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('achat/',views.achat),
    path('fournisseur/',views.fournisseur),
    path('listeAchat/',views.liste_achats),
    path('listeFournisseurs/',views.liste_fournisseurs),
]