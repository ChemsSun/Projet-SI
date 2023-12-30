from django.shortcuts import render ,redirect
from django.shortcuts import render

from SystemeGestion.models import Achat, Fournisseur, Produit
from .forms import AchatForm, FournisseurForm

def home(request):
    return render(request,'home.html')

def achat(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            fournisseur_nom=form.cleaned_data['fournisseur'].NomF
            produit_nom = form.cleaned_data['produit'].NomP
            quantite=form.cleaned_data['quantite']
            prix_unitaire=form.cleaned_data['prix_unitaire_ht']
            montant_total_achat=quantite * prix_unitaire
 
            fournisseur, created=Fournisseur.objects.get_or_create(NomF=fournisseur_nom)
            produit , created=Produit.objects.get_or_create(NomP=produit_nom)
            achat=Achat.objects.create(
                fournisseur=fournisseur,
                produit=form.cleaned_data['produit'],
                quantite=quantite,
                date_achat=form.cleaned_data['date_achat'],
                prix_unitaire_ht=prix_unitaire,
                montant_total_achat_ht =montant_total_achat,
                montant_paye=form.cleaned_data['montant_paye']
            )
            form.save()
            return redirect('liste_achats')
    else:
        form = AchatForm()
        message="remplire votre achat"
    return render(request, 'achat.html', {'form': form ,'message':message})

def fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseur.html', {'form': form})

def liste_achats(request):
    achats = Achat.objects.all()
    return render(request, 'liste_achats.html', {'achats': achats})

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'liste_fournisseurs.html', {'fournisseurs': fournisseurs})