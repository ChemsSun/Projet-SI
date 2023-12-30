from django.db import models

class Fournisseur(models.Model):
    ID_Fourni= models.AutoField(primary_key=True)
    NomF = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.NomF
    

class Produit(models.Model):
    Code=models.AutoField(primary_key=True)
    NomP=models.CharField(max_length=30)
    Description=models.CharField(max_length=100)
    def __str__(self):
        return self.NomP
    

class Achat(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_achat = models.DateField()
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2)
    montant_total_achat_ht = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.produit


class Client(models.Model):
    Code_Client=models.AutoField(primary_key=True)
    Nom=models.CharField(max_length=30)
    Prenom=models.CharField(max_length=30)
    Adress=models.CharField(max_length=50)
