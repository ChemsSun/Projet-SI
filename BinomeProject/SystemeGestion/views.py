from django.shortcuts import render ,redirect
from django.shortcuts import render

from SystemeGestion.models import Achat, Fournisseur
from .forms import AchatForm, FournisseurForm

def home(request):
    return render(request,'home.html')

def achat(request):
    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_achats')
    else:
        form = AchatForm()
    return render(request, 'achat.html', {'form': form})

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