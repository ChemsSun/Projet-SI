from django.db import models

class Fournisseur(models.Model):
    ID_Fourni= models.AutoField(primary_key=True)
    NomF = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    email = models.EmailField()
    solde = models.DecimalField(decimal_places=2, max_digits=10)
    
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
    montant_paye = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null=True)

    def __str__(self):
        return self.produit.NomP
    
    def montant_reste(self):
       return self.montant_total_achat_ht - self.montant_paye
    
class Client(models.Model):
    Code_Client=models.AutoField(primary_key=True)
    Nom=models.CharField(max_length=30)
    Prenom=models.CharField(max_length=30)
    Adress=models.CharField(max_length=50)


class Reglement_Fournisseur(models.Model):
    ID=models.AutoField(primary_key=True)
    # achat=models.ForeignKey(Achat,on_delete=models.CASCADE)
    fournisseur=models.ForeignKey(Fournisseur,on_delete=models.CASCADE)
    date_reglement=models.DateField()
    montant_versement=models.DecimalField(max_digits=10,decimal_places=2)

class Centre(models.Model):
    Code=models.AutoField(primary_key=True)
    designation=models.CharField(max_length=30)
    def __str__(self) -> str:
        return self.designation

class Transfert(models.Model):
    date_transfert=models.DateField()
    centre = models.CharField(max_length=100, choices=[('Centre 1', 'Centre 1'), ('Centre 2', 'Centre 2'), ('Centre 3', 'Centre 3')])
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    cout_transfert_equivalent = models.DecimalField(max_digits=10, decimal_places=2)