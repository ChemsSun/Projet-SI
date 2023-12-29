from django import forms
from .models import Achat, Fournisseur

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['fournisseur', 'produit', 'quantite', 'prix_unitaire_ht', 'date_achat']

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'adresse', 'email']    