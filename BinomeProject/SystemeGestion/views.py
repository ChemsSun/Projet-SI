from decimal import Decimal
from django.shortcuts import get_object_or_404, render ,redirect
from django.shortcuts import render
from django.db.models import Sum
from SystemeGestion.models import*
from .forms import*

def home(request):
    return render(request,'home.html')

#****************Achat***********************#
def achat(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            achat = form.save(commit=False)
            achat.montant_total_achat_ht = achat.quantite * achat.prix_unitaire_ht
            achat.matierePremiere.Qte+=form.cleaned_data['quantite']
            achat.matierePremiere.save()
            achat.save()
            return redirect('saisir_montant', achat_id=achat.CodeAchat)
    else:
        form = AchatForm()
    return render(request, 'achat/achat.html', {'form': form})

def saisir_montant(request, achat_id):
    achat = get_object_or_404(Achat, pk=achat_id)
    if request.method == 'POST':
        form = MontantForm(request.POST)
        if form.is_valid():
            achat.montant_paye = form.cleaned_data['montant_paye'] #mettre a jour le montant_paye a traver le montant saisie par le formulaire MontantForm
            if achat.montant_paye <= achat.montant_total_achat_ht:
                achat.fournisseur.solde=achat.fournisseur.solde+achat.montant_reste()
                achat.fournisseur.save()
            achat.save()
            return redirect('liste_achats')
    else:
        form = MontantForm()
    return render(request, 'achat/saisir_montant.html', {'form': form, 'achat': achat})

def liste_achats(request):
    achats = Achat.objects.all()
    myfilter=AchatFilter(request.GET, queryset=achats)
    achats = myfilter.qs
    return render(request, 'achat/liste_achats.html', {'achats': achats,'myfilter':myfilter})

def delete_achat(request,achat_id):
    achat=get_object_or_404(Achat,pk=achat_id)
    if request.method=='POST':
        achat.delete()
        return redirect('liste_achats')
    return render(request,'achat/delete_achat.html',{'achat':achat})

def modifier_achat(request,achat_id):
    modifier = Achat.objects.get(pk=achat_id)
    if request.method == 'POST':
        form = ModifierAchatForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect("liste_achats")
    else:
        form = FournisseurForm(instance=modifier)
    return render(request, 'achat/ModiAchat.html', {"form": form})
    

#****************Fournisseur***********************#

def fournisseur(request):
    if request.method == 'POST':    
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseur/fournisseur.html', {'form': form})

def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseur/liste_fournisseurs.html', {'fournisseurs': fournisseurs})

def delete_fournisseur(request,fournisseur_id):
    fournisseur=get_object_or_404(Fournisseur,pk=fournisseur_id)

    if request.method=='POST':
        fournisseur.delete()
        return redirect('liste_fournisseurs')
    return render(request,'fournisseur/delete_fournisseur.html',{'fournisseur':fournisseur})

def modifier_fournisseur(request,fournisseur_id):
    modifier = Fournisseur.objects.get(pk=fournisseur_id)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect("liste_fournisseurs")
    else:
        form = FournisseurForm(instance=modifier)

    return render(request, 'fournisseurModiFourni.html', {"form": form})

def reg(request,fournisseur_id):
    fournisseur=get_object_or_404(Fournisseur,pk=fournisseur_id)
    if request.method=='POST':
        form = Reglement(request.POST)
        if form.is_valid():
            montant_verser = form.cleaned_data['montant_versement']
            if montant_verser <= fournisseur.solde:
                fournisseur.solde -= montant_verser
                fournisseur.save()
                #modifier le règlement avant de l'enregistrer dans la base de données.
                reglement = form.save(commit=False)
                reglement.fournisseur = fournisseur
                reglement.save()

                return redirect('liste_fournisseurs')
    else:
        form = Reglement()
    return render(request, 'fournisseur/paiement.html', {'form': form})

def liste_reglement(request):
    reglements=Reglement_Fournisseur.objects.all()
    return render(request,'fournisseur/liste_reglement.html',{'reglements':reglements})

def delete_reglement(request,reglement_id):
    reglement=get_object_or_404(Reglement_Fournisseur,pk=reglement_id)

    if request.method=='POST':
        reglement.delete()
        return redirect('liste_reglement')
    return render(request,'fournisseur/delete_reglement.html',{'reglement':reglement})

#****************Matiere Premiere***********************#

def matierepremiere(request):
    if request.method=='POST':
        form=MatierePremiereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_matierepremiere')
    else:   
        form=MatierePremiereForm()
    return render(request,'matiere_premiere/produit.html',{'form':form})

def list_matierepremiere(request):
    produits=MatierePremiere.objects.all()
    return render(request,'matiere_premiere/liste_produits.html',{'produits':produits})

def delete_matierepremiere(request,produit_id):
    produit=get_object_or_404(MatierePremiere,pk=produit_id)
    if request.method=='POST':
        produit.delete()
        return redirect('liste_matierepremiere')
    return render(request,'matiere_premiere/delete_matierepr.html',{'produit':produit})

def modifier_matierepremiere(request, produit_id):
    modifier = MatierePremiere.objects.get(pk=produit_id)
    if request.method == 'POST':
        form = MatierePremiereForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect("list_matierepremiere")
    else:
        form = MatierePremiereForm(instance=modifier)

    return render(request, 'matiere_premiere/ModifMatiere.html', {"form": form})

#****************Transfert***********************#

def creer_transfert(request):
    if request.method == 'POST':
        form = TransfertForm(request.POST)
        if form.is_valid():
            transfert = form.save(commit=False)
            transfert.cout_transfert=transfert.matierePremiere.prix*transfert.quantite
            transfert.total+=transfert.cout_transfert
            transfert.save()
            return redirect('fiche_transferts')
    else:
        form = TransfertForm()
    return render(request, 'transfert/transfert.html', {'form': form})

def fiche_transferts(request):
    transferts = Transfert.objects.all()
    return render(request, 'transfert/fiche_transfert.html', {'transferts': transferts})

def fiche_transfert_centres(request,centre_id):
    transferts = Transfert.objects.filter(centre_id=centre_id)
    return render(request, 'transfert/fiche_transfert_centres.html', {'transferts': transferts})
#****************Centre***********************#

def creer_centre(request):
    if request.method=='POST':
        form=CentreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_centres')
    else:   
        form=CentreForm()
    return render(request,'centre/cree_centre.html',{'form':form})

def liste_centres(request):
    centres = Centre.objects.all()
    return render(request, 'centre/liste_centres.html', {'centres': centres})

def details_centre(request,centre_id):
    centre=get_object_or_404(Centre,pk=centre_id)
    return render(request, 'centre/details_centre.html', {'centre': centre})

#****************Employer***********************#
def employes(request, centre_id):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            nom_employe = form.cleaned_data['NomE']
            if Employe.objects.filter(NomE=nom_employe).exists():
                message="employe existe"
                return render(request, 'cree_employes.html', {'form': form, 'centre_id': centre_id, 'erreur': True,'message':message})
            employe = form.save(commit=False)
            employe.centre_id = centre_id
            employe.save()
            return redirect('list_employes', centre_id=centre_id)
    else:
        form = EmployeForm()
    return render(request, 'centre/cree_employes.html', {'form': form, 'centre_id': centre_id})

def list_employes(request, centre_id):
    employes = Employe.objects.filter(centre_id=centre_id)
    return render(request, 'centre/liste_employes.html', {'employes': employes, 'centre_id': centre_id})

def delete_emloyes(request,employe_id):
    employe=get_object_or_404(Employe,pk=employe_id)
    if request.method=='POST':
       employe.delete()
       return redirect('list_employes')
    return render(request,'centre/delete_employe.html',{'employe':employe})
#****************Paiment Emloyes***********************#
def paiment_journalier(request,employe_id):
    employe=Paiement_Emloyes.objects.get(pk=employe_id)
    form=PaimentEmpoye(request.POST)
    if form.is_valid():
       paiment=form.save(commit=False)
       paiment.employe=employe
       paiment.save()
       return redirect('list_employes')
    else:
        return render(request,'centre/paiement_emp.html',{'form':form})