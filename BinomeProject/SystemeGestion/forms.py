from django import forms
from .models import*
import django_filters
from django.utils.translation import gettext_lazy as _
from django_select2 import forms as s2forms 

class FournisseurWidget(s2forms.ModelSelect2Widget):
    model = Fournisseur  # Ajoutez cette ligne pour spécifier le modèle
    search_fields = [
        'NomF__icontains',
    ]

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
        model = Achat
        fields = ['fournisseur', 'matierePremiere', 'quantite', 'prix_unitaire_ht', 'date_achat']
        labels = {
            'matierePremiere': _("Matière première :"),
            'quantite': _("Quantité :"),
            'prix_unitaire_ht': _("Prix Unitaire :"),
            'date_achat': _("Date achat :"),
        }
        widgets = {
            'date_achat': forms.DateInput(attrs={'type': 'date'}),
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['NomF', 'adresse', 'email']    
        labels={
            'NomF':_("Nom  :"),
            'adresse':_("Adresse :"),
            'email':_("Email :"),
        }

class FournisseurFilter(django_filters.FilterSet):
    class Meta:
        model=Fournisseur
        fields= ['NomF']
        labels={
            'NomF':_("Nom Fournisseur :"),
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
        widgets={
            'fournisseur':FournisseurWidget
        }

class TransfertFilter(django_filters.FilterSet):
    class Meta:
        model = Transfert
        fields = ['date_transfert', 'centre', 'matierePremiere']
        labels = {
            'date_transfert': _("Date du transfert :"),
            'centre': _("Centres :"),
            'matierePremiere': _("Nom de Matiere :")
        }

class VenteFilter(django_filters.FilterSet):
    class Meta:
        model=Vente
        fields=['Client','mtrP']
        labels={
            'Client':_("Client :"),
            'mtrP':_("Matiere Premiere :")
        }

class VenteCFilter(django_filters.FilterSet):
    class Meta:
        model=VenteC
        fields=['Client']
        labels={
            'Client':_("Client :"),
        }

class VenteCForm(forms.ModelForm):
    class Meta:
        model=VenteC
        fields=['Client', 'prdt'] 
        Labels={
            'Client':_("Client :"),
            'prdt':_("Produit :"),
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
        fields=['presence','date_paiement','salaire_journalier','salaire_retenu','masrouf']
        labels={
            'presence':_("Presence"),
            'date_paiement':_("Date :"),
            'salaire_journalier':_("salaire_journalier est :"),
            'salaire_retenu':_("salaire_retenu est :"),
            'masrouf':_("Valeur du masrouf donné est :"),
        }




class ClientForm(forms.ModelForm):
    class Meta:
       model = Client
       fields = ['Nom','Prenom','Adress']   
       labels={
           'Nom':_("Nom :"),
           'Prenom':_("Prenom :"),
           'Adress':_("Adress :"),
       }
   
class VenteForm(forms.ModelForm):
    class Meta:
        model =Vente
        fields = ['Client', 'mtrP', 'qte', 'price']
        labels={
           'Client':_("Client :"),
           'mtrP':_("Matiere Premiere :"),
           'qte':_("Quantité :"),
           'price':_("Prix :"),
       }

class ReglementForm(forms.Form):
    montant_paye = forms.FloatField(label='Montant Payé')
    

class ModifierVenteForm(forms.ModelForm):
    class Meta:
        model=Vente
        fields=['Client', 'mtrP', 'qte', 'price']
        labels={
           'Client':_("Client :"),
           'mtrP':_("Matiere Premiere :"),
           'qte':_("Quantité :"),
           'price':_("Prix :"),
       }


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['Nom', 'date_production','designation','Quantite','price_v']  
        Labels={
            'Nom':_("Nom :"),
            'date_production':_("Date de production :"),
            'designation':_("Designation :"),
            'Quantite':_("Quantité :"),
            'price_v':_("Prix de vente :"),  
        }  


class ModifierProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=[ 'Nom', 'date_production','designation','Quantite','price_v']
        Labels={
            'Nom':_("Nom :"),
            'date_production':_("Date de production :"),
            'designation':_("Designation :"),
            'Quantite':_("Quantité :"),
            'price_v':_("Prix de vente :"),  
        } 

class VenteCForm(forms.ModelForm):
    class Meta:
        model=VenteC
        fields=['Client', 'prdt', 'qte', 'price']   
        Labels={
            'Client':_("Client :"),
            'prdt':_("Produit :"),
            'qte':_("Quantité :"),
            'price':_("Prix :"),
        } 

class ModifierVenteC(forms.ModelForm):
    class Meta:
        model=VenteC
        fields=['Client', 'prdt', 'qte', 'price']  
        Labels={
            'Client':_("Client :"),
            'prdt':_("Produit :"),
            'qte':_("Quantité :"),
            'price':_("Prix :"),  
        } 