from django import forms
from .models import Achat, Fournisseur,Produit

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['fournisseur', 'produit', 'quantite', 'prix_unitaire_ht', 'date_achat','montant_paye']

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['NomF', 'adresse', 'email']    

class ProduitForm(forms.ModelForm):
    class Meta:
        model=Produit
        fields = ['NomP','Description','prix_achat']