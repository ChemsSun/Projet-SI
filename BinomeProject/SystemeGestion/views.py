from decimal import Decimal
from django.shortcuts import get_object_or_404, render ,redirect
from django.shortcuts import render

from SystemeGestion.models import Achat, Fournisseur, Produit
from .forms import AchatForm, FournisseurForm, ProduitForm

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
            # Pas besoin de créer manuellement l'objet Achat
            form.save()
            return redirect('liste_achats')
    else:
        form = AchatForm()
        message = "Remplissez votre achat"
    return render(request, 'achat.html', {'form': form, 'message': message})

def fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseur.html', {'form': form})

# def paiement(request,achat_id):
#     achat = get_object_or_404(Achat, pk=achat_id)
#     montant_paye=request.POST.get('montant_paye')
#     achat.montant_paye += Decimal(montant_paye)
#     achat.save()
#     achat.fournisseur.solde -= Decimal(montant_paye)
#     achat.fournisseur.save()
#     return render(request,'paiement.html',{'achat':achat})

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