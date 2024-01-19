from django import forms
from .models import*
import django_filters
from django.utils.translation import gettext_lazy as _

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['fournisseur', 'matierePremiere', 'quantite', 'prix_unitaire_ht', 'date_achat']
        labels={
            'fournisseur':_("Fournisseur :"),
            'matierePremiere':_("Matière première :"),
            'quantite':_("Quantité :"),
            'prix_unitaire_ht':_("Prix Unitaire :"),
            'date_achat':_("Date achat :"),
        }

class ModifierAchatForm(forms.ModelForm):
    class Meta:
        model=Achat
        fields=['fournisseur','matierePremiere','quantite', 'prix_unitaire_ht', 'date_achat','montant_paye']

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['NomF', 'adresse', 'email']    
        labels={
            'NomF':_("Nom  :"),
            'adresse':_("Adresse :"),
            'email':_("Email :"),
        }

class MatierePremiereForm(forms.ModelForm):
    class Meta:
        model=MatierePremiere
        fields = ['NomP','Description']
        labels={
            'NomP':_("Nom de la matière :"),
            'Description':_("Description :"),
        }

class AchatFilter(django_filters.FilterSet):
    class Meta:
        model=Achat
        fields= ['fournisseur', 'matierePremiere','date_achat']
        labels={
            'fournisseur':_("Fournisseur :"),
            'matierePremiere':_("Matière première :"),
            'date_achat':_("Date :"),
        }

class MontantForm(forms.ModelForm):
    class Meta:
        model =Achat
        fields=['montant_paye']
        labels={
            'montant_paye':_("Montant à paye :"),
        }

class Reglement(forms.ModelForm):
    class Meta:
        model=Reglement_Fournisseur
        fields=['date_reglement','montant_versement']
        error_messages = {
            'date_reglement':{'required':''},
            'montant_versement':{'required':''}
        }
        labels={
            'date_reglement':_("Date :"),
            'montant_versement':_("Montant_versement :"),
        }

class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['date_transfert', 'centre', 'matierePremiere', 'quantite']
        labels={
            'date_transfert':_("Date :"),
            'centre':_("Centre :"),
            'matierePremiere':_("La matière:"),
            'quantite':_("Quantité transferer "),
        }

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = ['designation']

class EmployeForm(forms.ModelForm):
    class Meta:
        model=Employe
        fields=['NomE','AdrE','Email','Tlf']
        labels={
            'NomE':_("Nom :"),
            'AdrE':_("Adresse  :"),
            'Email':_("Email:"),
            'Tlf':_("Numero de telephone "),
        }

class PaimentEmpoye(forms.ModelForm):
    class Meta:
        model=Paiement_Emloyes
        fields=['presence','salaire_journalier','salaire_retenu','masrouf']
        labels={
            'presence':_("Presence"),
            'salaire_journalier':_("salaire_journalier est :"),
            'salaire_retenu':_("salaire_retenu est :"),
            'masrouf':_("Valeur du masrouf donné est :"),
        }