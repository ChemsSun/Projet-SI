from django import forms
from .models import*

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['fournisseur', 'matierePremiere', 'quantite', 'prix_unitaire_ht', 'date_achat']

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['NomF', 'adresse', 'email']    

class MatierePremiereForm(forms.ModelForm):
    class Meta:
        model=MatierePremiere
        fields = ['NomP','Description']
    
class MontantForm(forms.ModelForm):
    class Meta:
        model =Achat
        fields=['montant_paye']

class Reglement(forms.ModelForm):
    class Meta:
        model=Reglement_Fournisseur
        fields=['fournisseur','date_reglement','montant_versement']
        error_messages = {
            'fournisseur': {'required': ''},
            'date_reglement':{'required':''},
            'montant_versement':{'required':''}
        }
class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['date_transfert', 'centre', 'matierePremiere', 'quantite']

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = ['designation']