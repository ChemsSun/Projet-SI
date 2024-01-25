from datetime import date
import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404, render ,redirect
from django.shortcuts import render
from django.db.models import Sum
from SystemeGestion.models import*
from .forms import*

def home(request):
    return render(request,'home.html')

#****************Gestion des achats***********************#
def achat(request): 
    if request.method == 'POST':
        #tester si le formulaire est POST
        form = AchatForm(request.POST)  
        if form.is_valid():  
            #commit=False veut dire ne pas enrengistrer l'achat jusqu'a faire le traitement qu'on veut
            achat = form.save(commit=False)  
            #calcul du monatant total
            achat.montant_total_achat_ht = achat.quantite * achat.prix_unitaire_ht
            #affecter la quantité acheter à la quantite existante dans le stock de matiere premiere   
            achat.matierePremiere.Qte+=form.cleaned_data['quantite']  
            achat.matierePremiere.prix=form.cleaned_data['prix_unitaire_ht']  
            #enrengistrer les modification du stock de la matiere premiere
            achat.matierePremiere.save()   
            #enrengistrer l'achat
            achat.save()  
            #rediriger l'achat à la vue "saisir_montant"
            return redirect('saisir_montant', achat_id=achat.CodeAchat)  
    else:
        form = AchatForm()
    return render(request, 'achat/achat.html', {'form': form})

def saisir_montant(request, achat_id):
    achat = get_object_or_404(Achat, pk=achat_id)
    if request.method == 'POST':
        form = MontantForm(request.POST)
        if form.is_valid():
            #mettre a jour le montant_paye a traver le montant saisie par le formulaire MontantForm
            achat.montant_paye = form.cleaned_data['montant_paye'] 
            #si le montant paye est inferieur au montant total d'achat alors MAJ le solde et le montant restant de l'achat
            if achat.montant_paye <= achat.montant_total_achat_ht:
                achat.fournisseur.solde=achat.fournisseur.solde+achat.montant_reste()
                achat.fournisseur.save()
            achat.save()
            return redirect('liste_achats')
    else:
        form = MontantForm()
    return render(request, 'achat/saisir_montant.html', {'form': form, 'achat': achat})

def liste_achats(request):
    achats = Achat.objects.all().order_by('matierePremiere__NomP')
    #affecter un filtre à la liste des achats selon les donner du AchatFilter
    myfilter=AchatFilter(request.GET, queryset=achats)
    achats = myfilter.qs
    return render(request, 'achat/liste_achats.html', {'achats': achats,'myfilter':myfilter})

def delete_achat(request,achat_id):
    #cette methode permet le renvoie d'une exception si l'objet demander n'existe pas 
    achat=get_object_or_404(Achat,pk=achat_id)
    if request.method=='POST':
        #.delte() permet de supprimet l'achat correspondant
        achat.delete()
        achat.matierePremiere.Qte -= achat.quantite
        return redirect('liste_achats')
    return render(request,'achat/delete_achat.html',{'achat':achat})

def modifier_achat(request,achat_id):
    modifier = Achat.objects.get(pk=achat_id)
    #modifier l'achat correspondant au achat_id
    form = ModifierAchatForm(request.POST or None, instance=modifier)
    if form.is_valid():
        form.save()
        return redirect("liste_achats")
    return render(request, 'achat/ModiAchat.html', {"form": form,"modifier":modifier})
    
#****************Fournisseur***********************#

def fournisseur(request):   #meme traitement comme achat
    if request.method == 'POST':    
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_fournisseurs')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseur/fournisseur.html', {'form': form})

def liste_fournisseurs(request):
    #.order_by permet de trier la liste par le nom du fournisseur
    fournisseurs = Fournisseur.objects.all().order_by('NomF') 
    myfilter=FournisseurFilter(request.GET, queryset=fournisseurs)
    fournisseurs = myfilter.qs
    return render(request, 'fournisseur/liste_fournisseurs.html', {'fournisseurs': fournisseurs,'myfilter':myfilter})

def delete_fournisseur(request,fournisseur_id):
    fournisseur=get_object_or_404(Fournisseur,pk=fournisseur_id)
    if request.method=='POST':
        fournisseur.delete()
        return redirect('liste_fournisseurs')
    return render(request,'fournisseur/delete_fournisseur.html',{'fournisseur':fournisseur})

def modifier_fournisseur(request,fournisseur_id):
       # Récupère le fournisseur à partir de son ID.
    modifier = Fournisseur.objects.get(pk=fournisseur_id)
    # Si la requête est en POST, traite les données du formulaire.
    if request.method == 'POST':
         # Crée un formulaire à partir des données du formulaire.
        form = FournisseurForm(request.POST, instance=modifier)
        # Si le formulaire est valide, enregistre les modifications.
        if form.is_valid():
            form.save()
             # Redirige vers la liste des fournisseurs.
            return redirect("liste_fournisseurs")
          # Sinon, crée un formulaire vide.
    else:
        form = FournisseurForm(instance=modifier)
        # Renvoie la réponse HTTP.
    return render(request, 'fournisseur/ModiFourni.html', {"form": form,"modifier":modifier})

def reg(request,fournisseur_id):
    fournisseur=get_object_or_404(Fournisseur,pk=fournisseur_id)
    if request.method=='POST':
        form = Reglement(request.POST)
        if form.is_valid():
             # Récupère le montant du versement.
            montant_verser = form.cleaned_data['montant_versement']
            # Vérifie que le montant du versement est inférieur ou égal au solde du fournisseur.
            if montant_verser <= fournisseur.solde:
                  # Met à jour le solde du fournisseur.
                fournisseur.solde -= montant_verser
                fournisseur.save()
                #modifier le règlement avant de l'enregistrer dans la base de données.
                reglement = form.save(commit=False)
                reglement.fournisseur = fournisseur
                reglement.save()

                return redirect('liste_fournisseurs')
    else:
        form = Reglement()
    return render(request, 'fournisseur/reglement.html', {'form': form,'fournisseur':fournisseur})

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
             # Extraire le nom de la matiere premiere a partir du cleaned_data.
            nom_matiere=form.cleaned_data['NomP']
            # verifier s'il existe un meme nom qui existe déjà
            if MatierePremiere.objects.filter(NomP=nom_matiere).exists():
                message="Produit existe"
                return render(request, 'matiere_premiere/produit.html', {'form': form,'erreur': True,'message':message})
            form.save()
            return redirect('list_matierepremiere')
    else:   
        form=MatierePremiereForm()
    return render(request,'matiere_premiere/produit.html',{'form':form})

def list_matierepremiere(request):
    produits=MatierePremiere.objects.all().order_by('NomP')
    #calcule le total des prix de tous les matiere premiere 
    somme_prix_total = sum(produit.prix for produit in produits)
    somme_quantite=sum(produit.Qte for produit in produits)
    somme_vente=sum(produit.prix_vente for produit in produits)
    return render(request,'matiere_premiere/liste_produits.html',{'produits':produits,'somme_prix_total':somme_prix_total,'somme_quantite':somme_quantite,'somme_vente':somme_vente})

def delete_matierepremiere(request, produit_id):
    produit = get_object_or_404(MatierePremiere, pk=produit_id)
    if request.method == 'POST':
        produit.delete()
    return redirect('list_matierepremiere')  # Redirige vers la liste après suppression
    
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

#****************Gestion de Transfert***********************#

def creer_transfert(request):
    message = ""  # Initialiser le message en dehors des branches conditionnelles

    if request.method == 'POST':
        form = TransfertForm(request.POST)
        if form.is_valid():
            # Créer un transfert sans l'enregistrer encore
            transfert = form.save(commit=False)
            # Calculer le coût du transfert
            transfert.cout_transfert = transfert.matierePremiere.prix * transfert.quantite
            # Mettre à jour la quantité de la matière première
            matiere_premiere = get_object_or_404(MatierePremiere, pk=transfert.matierePremiere.pk)
            if matiere_premiere.Qte < form.cleaned_data['quantite']:
                message = "Pas de quantité suffisante"
            else:
                matiere_premiere.Qte -= form.cleaned_data['quantite']
                matiere_premiere.save()

                # Mettre à jour le total du transfert
                transfert.total += transfert.cout_transfert
                transfert.save()
                message = "Transfert effectué avec succès"

    else:
        form = TransfertForm()

    return render(request, 'transfert/transfert.html', {'form': form, 'message': message})

def fiche_transferts(request):
    transferts = Transfert.objects.all().order_by('matierePremiere__NomP')
     # Calcule le total de tous les transferts.
    total_transferts = Transfert.objects.aggregate(Sum('total'))['total__sum'] or 0
    # Crée un filtre pour la liste des transferts.
    myfilter=TransfertFilter(request.GET, queryset=transferts)
    transferts = myfilter.qs
     # Applique le filtre à la liste des transferts.
    return render(request, 'transfert/fiche_transfert.html', {'transferts': transferts,'myfilter':myfilter, 'total_transferts': total_transferts})

def fiche_transfert_centres(request,centre_id):
    transferts = Transfert.objects.filter(centre_id=centre_id)
    myfilter=TransfertFilter(request.GET, queryset=transferts)
    transferts = myfilter.qs
    return render(request, 'transfert/fiche_transfert_centres.html', {'transferts': transferts,'myfilter':myfilter})
#****************Gestion de Centre***********************#
def liste_centres(request):
    if Centre.objects.count() == 0:
        Centre.objects.create(designation='centre1')
        Centre.objects.create(designation='centre2')
        Centre.objects.create(designation='centre3')
    centres = Centre.objects.all()
    context = {'centres': centres}
    return render(request, 'home.html',context)

def details_centre(request,centre_id):
    centre=get_object_or_404(Centre,pk=centre_id)
    return render(request, 'centre/details_centre.html', {'centre': centre})

#****************Employer***********************#
def employes(request, centre_id):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            nom_employe = form.cleaned_data['NomE']
            # Vérifier si un employé avec le même nom existe déjà
            if Employe.objects.filter(NomE=nom_employe).exists():
                message="employe existe"
                return render(request, 'centre/cree_employes.html', {'form': form, 'centre_id': centre_id, 'erreur': True,'message':message})
            # Créer un nouvel employé
            employe = form.save(commit=False)
             # Assigner l'employé au centre donné
            employe.centre_id = centre_id
            employe.save()
            return redirect('list_employes', centre_id=centre_id)
    else:
        form = EmployeForm()
    return render(request, 'centre/cree_employes.html', {'form': form, 'centre_id': centre_id})

def list_employes(request, centre_id):
    employes = Employe.objects.filter(centre_id=centre_id).order_by('NomE')
    return render(request, 'centre/liste_employes.html', {'employes': employes, 'centre_id': centre_id})

def delete_emloyes(request,employe_id):
    employe=get_object_or_404(Employe,pk=employe_id)
    if request.method=='POST':
       employe.delete()
    return redirect("list_employes", centre_id=employe.centre_id)

def modifier_employe(request,employe_id):
    modifier = Employe.objects.get(pk=employe_id)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect("list_employes", centre_id=modifier.centre_id)
    else:
        form = EmployeForm(instance=modifier)

    return render(request, 'centre/ModifEmploye.html', {"form": form})
#****************Paiment Emloyes***********************#
def paiment_journalier(request, employe_id):
    employe = Employe.objects.get(pk=employe_id)
    paiements = Paiement_Emloyes.objects.filter(employe=employe)
    TotalJournilier = 0
    TotalMasrouf = 0
    TotalRetenue = 0
    message = ""

    if request.method == 'POST':
        form = PaimentEmpoye(request.POST)
        if form.is_valid():
            cpt = paiements.count()

            if cpt < 31:

                # Ajouter un nouveau paiement
                Paiement_Emloyes.objects.create(
                    employe=employe,
                    date_paiement=form.cleaned_data['date_paiement'],
                    presence=form.cleaned_data['presence'],
                    salaire_journalier=form.cleaned_data['salaire_journalier'],
                    salaire_retenu=form.cleaned_data['salaire_retenu'],
                    masrouf=form.cleaned_data['masrouf']
                )

                TotalJournilier += form.cleaned_data['salaire_journalier']
                TotalRetenue += form.cleaned_data['salaire_retenu']
                TotalMasrouf += form.cleaned_data['masrouf']
                employe.Salaire += TotalJournilier - TotalRetenue - TotalMasrouf
                employe.save()

                if cpt + 1 ==31 :
                    message = "Fin du mois"
            else:
                message = "Vous avez atteint le nombre maximum de paiements pour ce mois."

    else:
        form = PaimentEmpoye()

    return render(request, 'centre/paiement_emp.html', {'employe': employe, 'form': form, 'paiements': paiements, 'message': message})

# *************Gestion des Ventes***********************************#
def vendre(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save()

            # Créer un crédit client pour cette vente
            credit_client = CreditClient.objects.create(
                client=vente.Client,
                montant_vente=vente.montant_vente,
                montant_paye=0,  # Initialiser le montant payé à zéro
                montant_restant=vente.montant_vente
            )
            vente.credit_client = credit_client
            vente.save()
            matiere_premiere = MatierePremiere.objects.get(pk=vente.mtrP.Code)
            matiere_premiere.Qte -= vente.qte  # Retirer la quantité vendue du stock
            matiere_premiere.save()

            # Mettre à jour le prix de vente de la matière première
            matiere_premiere.prix_vente = vente.price
            matiere_premiere.save()

            return redirect('reglement', vente.codevente)  # Rediriger vers la page de règlement avec l'ID de la vente
    else:
        form = VenteForm()

    clients = Client.objects.all()
    return render(request, 'vente/vente.html', {'form': form, 'clients': clients})

def journal_vente(request):
    vendus = Vente.objects.all()
    myfilter=VenteFilter(request.GET, queryset=vendus)
    vendus = myfilter.qs
    return render(request, 'vente/journal_vente.html', {'vendus': vendus,'myfilter':myfilter})

def reglement(request, vente_id):
    vente = Vente.objects.get(pk=vente_id)
    credit_client = vente.credit_client

    if request.method == 'POST':
        reglement_form = ReglementForm(request.POST)
        if reglement_form.is_valid():
            montant_paye = reglement_form.cleaned_data['montant_paye']

            # Mettre à jour le crédit client
            credit_client.montant_paye += montant_paye
            credit_client.montant_restant = vente.montant_vente - credit_client.montant_paye
            credit_client.save()

            return redirect('journal_vente')
    else:
        reglement_form = ReglementForm()

    return render(request, 'vente/reglement.html', {'vente': vente, 'credit_client': credit_client, 'reglement_form': reglement_form})

def liste_reglements(request):
    reglements = CreditClient.objects.all()
    return render(request, 'vente/liste_reglementsC.html', {'reglements': reglements})

def modifier_vente(request,vente_id):
    modifier = Vente.objects.get(pk=vente_id)
    if request.method == 'POST':
        form = ModifierVenteForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect("journal_vente")
    else:
        form = ModifierVenteForm(instance=modifier)
    return render(request, 'vente/ModifierVente.html', {"form": form})

def delete_vente(request,vente_id):
    vente=get_object_or_404(Vente,pk=vente_id)
    if request.method=='POST':
        vente.delete()
        return redirect('journal_vente')
    return render(request,'vente/SupprimerVente.html',{'vente':vente})
# *************Gestion des Clients***********************************#
def modifier_client(request,client_id):
    modifier = Client.objects.get(pk=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect('listeclient')
    else:
        form = ClientForm(instance=modifier)

    return render(request, 'vente/ModifierClient.html', {"form": form})

def client(request):
    if request.method =='POST':    
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeclient')
    else:
         form = ClientForm()
    return render(request, 'vente/AjoutClient.html', {'form': form})

def supp_client(request,client_id):
    client=get_object_or_404(Client,pk=client_id)
    if request.method=='POST':
        client.delete()
        return redirect('listeclient')
    return render(request,'vente/SuppClient.html',{'client':client})

def listeclient(request):
    clients = Client.objects.all()
    return render(request, 'vente/listeclient.html', {'clients': clients})

#***************Produits centres************************************#
def production(request,centre_id):
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            Product=form.save(commit=False)
            # Assigner le produit au centre donné
            Product.centre_id = centre_id
            Product.save()
            return redirect('listeP', centre_id=centre_id)
    else:   
        form=ProductForm()
    return render(request,'Production/AjoutP.html',{'form':form})

def list_P(request,centre_id):
    products=Product.objects.filter(centre_id=centre_id)
    return render(request,'Production/listeP.html',{'products':products,'centre_id': centre_id})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
    return redirect('listeP',centre_id=product.centre_id)  # Redirige vers la liste après suppression
    
def modifier_product(request, product_id):
    modifier = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect('listeP',centre_id=modifier.centre_id)
    else:
        form = ModifierProductForm(instance=modifier)

    return render(request, 'Production/ModifP.html', {"form": form})

# *************Gestion des Ventes centres ***********************************#
def ventec(request,centre_id):
    if request.method=='POST':
        form=VenteCForm(request.POST)
        if form.is_valid():
            vendu=form.save(commit=False)
            # Assigner le produit au centre donné
            vendu.centre_id = centre_id
            vendu.save()
            return redirect('listeV', centre_id=centre_id)
    else:   
        form=VenteCForm()
    return render(request,'centre/AjoutV.html',{'form':form})

def list_V(request,centre_id):
    ventes=VenteC.objects.filter(centre_id=centre_id)
    myfilter=VenteCFilter(request.GET, queryset=ventes)
    ventes = myfilter.qs
    return render(request,'centre/journal_vntC1.html',{'ventes':ventes,'centre_id': centre_id,'myfilter':myfilter})

def delete_V(request, VenteC_id):
    venteC= get_object_or_404(VenteC, pk=VenteC_id)
    if request.method == 'POST':
        venteC.delete()
    return redirect('listeV',centre_id=venteC.centre_id)  # Redirige vers la liste après suppression
    
def modifier_V(request, VenteC_id):
    modifier = VenteC.objects.get(pk=VenteC_id)
    if request.method == 'POST':
        form = VenteCForm(request.POST, instance=modifier)
        if form.is_valid():
            form.save()
            return redirect('listeV',centre_id=modifier.centre_id)
    else:
        form = ModifierVenteC(instance=modifier)
    return render(request, 'centre/ModifV.html', {"form": form})



def dashboard(request):
    tops_clients = Client.objects.all().order_by('-vente__montant_vente')[:5]

    # Utilisez le champ correct pour ordonner les fournisseurs par montant d'achat
    tops_fournisseurs = Fournisseur.objects.all().order_by('-achat__montant_total_achat_ht')[:5]

    total_achats = Achat.objects.aggregate(total=models.Sum('montant_total_achat_ht'))['total'] or 0
    total_ventes = Vente.objects.aggregate(total=models.Sum('montant_vente'))['total'] or 0

    # Convertissez les résultats en float avant de faire la division
    total_achats = float(total_achats)
    total_ventes = float(total_ventes)

    taux_achats = (total_achats / total_ventes)  if total_ventes != 0 else 0
    taux_ventes = (total_ventes / total_achats)  if total_achats != 0 else 0

    context = {
        'tops_clients': tops_clients,
        'tops_fournisseurs': tops_fournisseurs,
        'taux_achats': taux_achats,
        'taux_ventes': taux_ventes,
    }

    return render(request, 'dashboard.html', context)

