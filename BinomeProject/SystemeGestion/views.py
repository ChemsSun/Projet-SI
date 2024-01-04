from decimal import Decimal
from django.shortcuts import get_object_or_404, render ,redirect
from django.shortcuts import render

from SystemeGestion.models import Achat, Fournisseur, Produit, Reglement_Fournisseur
from .forms import AchatForm, FournisseurForm, MontantForm, ProduitForm, Reglement, TransfertForm
from .import forms
def home(request):
    return render(request,'home.html')

# def achat(request):
#     if request.method == 'POST':
#         form = AchatForm(request.POST)
#         if form.is_valid():
#             fournisseur_nom = form.cleaned_data['fournisseur'].NomF
#             produit_nom = form.cleaned_data['produit'].NomP
#             quantite = form.cleaned_data['quantite']
#             prix_unitaire_ht = form.cleaned_data['prix_unitaire_ht']
#             montant_paye = form.cleaned_data['montant_paye']
#             montant_total_achat_ht = quantite * prix_unitaire_ht
 
#             fournisseur, created=Fournisseur.objects.get_or_create(NomF=fournisseur_nom)
#             achat=Achat.objects.create(
#                 fournisseur=fournisseur,
#                 produit=form.cleaned_data['produit'],
#                 quantite=quantite,
#                 date_achat=form.cleaned_data['date_achat'],
#                 prix_unitaire_ht=prix_unitaire_ht,
#                 montant_total_achat_ht=montant_total_achat_ht,
#                 montant_paye=montant_paye
#             )
#             form.save()
#             return redirect('liste_achats')
#     else:
#         form = AchatForm()
#         message="remplire votre achat"
#     return render(request, 'achat.html', {'form': form ,'message':message})



def achat(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            achat = form.save(commit=False)
            achat.montant_total_achat_ht = achat.quantite * achat.prix_unitaire_ht
            achat.save()
            return redirect('saisir_montant', achat_id=achat.id)
    else:
        form = AchatForm()
    return render(request, 'achat.html', {'form': form})

def saisir_montant(request, achat_id):
    achat = get_object_or_404(Achat, pk=achat_id)
    if request.method == 'POST':
        form = MontantForm(request.POST)
        if form.is_valid():
            achat.montant_paye = form.cleaned_data['montant_paye'] #mettre a jour le montant_paye a traver le montant saisie par le formulaire MontantForm
            if achat.montant_paye <= achat.montant_total_achat_ht:
                achat.fournisseur.solde=achat.montant_reste()
                achat.fournisseur.save()
            achat.save()
            return redirect('liste_achats')
    else:
        form = MontantForm()
    return render(request, 'saisir_montant.html', {'form': form, 'achat': achat})

def fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseur.html', {'form': form})


# def paiement(request, achat_id):
#     achat = get_object_or_404(Achat, pk=achat_id)

#     if request.method == 'POST':
#         montant_paye = request.POST.get('montant_paye')
#         if montant_paye:
#             montant_paye = Decimal(montant_paye)

#             if montant_paye >= achat.montant_reste():
#                 achat.montant_paye = achat.montant_total_achat_ht
#             else:
#                 achat.montant_paye += montant_paye
#             achat.save()
#             achat.fournisseur.solde -= montant_paye
#             achat.fournisseur.save()
#     return render(request, 'paiement.html', {'achat': achat})
def reg(request,fournisseur_id):
    fournisseur=get_object_or_404(Fournisseur,pk=fournisseur_id)
    if request.method=='POST':
        form = Reglement(request.POST)
        if form.is_valid():
             montant_verser=Reglement_Fournisseur.montant_versement
             if montant_verser < Achat.montant_reste():
               fournisseur.solde -=montant_verser
               fournisseur.solde.save()
               form.save()
               return redirect('liste_fournisseurs')
    else:
        form = Reglement()
    return render(request, 'paiement.html', {'form': form})
# def Reglement_Fournisseur(request,achat_id):
#     achat=get_object_or_404(Achat,pk=achat_id)
#     if request.method=='POST':
#         form=Reglement(request.POST)
#         if form.is_valid():
#             reglement = form.save(commit=False)
#             reglement.achat = achat
#             reglement.save()
#             return redirect('liste_achats')
#     else:   
#         form=Reglement()
#     return render(request,'paiement.html',{'form':form})


def produits(request):
    if request.method=='POST':
        form=ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_produit')
    else:   
        form=ProduitForm()
    return render(request,'produit.html',{'form':form})

def list_produit(request):
    produits=Produit.objects.all()
    return render(request,'liste_produits.html',{'produits':produits})

def liste_achats(request):
    achats = Achat.objects.all()
    return render(request, 'liste_achats.html', {'achats': achats})

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'liste_fournisseurs.html', {'fournisseurs': fournisseurs})

def delete_fournisseur(request,fournisseur_id):
    fournisseur=get_object_or_404(Fournisseur,pk=fournisseur_id)

    if request.method=='POST':
        fournisseur.delete()
        return redirect('liste_fournisseurs')
    return render(request,'delete_fournisseur.html',{'fournisseur':fournisseur})

def delete_Produit(request,produit_id):
    produit=get_object_or_404(Produit,pk=produit_id)

    if request.method=='POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request,'delete_Produit.html',{'produit':produit})

def delete_achat(request,achat_id):
    achat=get_object_or_404(Achat,pk=achat_id)
    if request.method=='POST':
        achat.delete()
        return redirect('liste_achats')
    return render(request,'delete_achat.html',{'achat':achat})

def creer_transfert(request):
    if request.method == 'POST':
        form = TransfertForm(request.POST)
        if form.is_valid():
            transfert = form.save(commit=False)
            transfert.cout_transfert = transfert.produit.p * transfert.quantite
            transfert.save()
            return redirect('fichetransferts')
    else:
        form = TransfertForm()
    return render(request, 'transfert.html', {'form': form})

def fiche_transferts(request):
    transferts = TransfertForm.objects.all()
    return render(request, 'fiche_transfert.html', {'transferts': transferts})