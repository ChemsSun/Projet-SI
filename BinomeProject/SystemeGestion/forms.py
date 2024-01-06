from django import forms
from .models import Achat, Fournisseur,Produit, Reglement_Fournisseur, Transfert

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['fournisseur', 'produit', 'quantite', 'prix_unitaire_ht', 'date_achat']

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['NomF', 'adresse', 'email']    

class ProduitForm(forms.ModelForm):
    class Meta:
        model=Produit
        fields = ['NomP','Description']
    
class MontantForm(forms.ModelForm):
    class Meta:
        model =Achat
        fields=['montant_paye']

class Reglement(forms.ModelForm):
    class Meta:
        model=Reglement_Fournisseur
        fields=['fournisseur','date_reglement','montant_versement']

class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['date_transfert', 'centre', 'produit', 'quantite']