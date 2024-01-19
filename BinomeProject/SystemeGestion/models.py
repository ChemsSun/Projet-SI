from django.db import models

class Fournisseur(models.Model):
    ID_Fourni= models.AutoField(primary_key=True)
    NomF = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    email = models.EmailField()
    solde = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    
    def __str__(self):
        return self.NomF


class MatierePremiere(models.Model):
    Code=models.AutoField(primary_key=True)
    NomP=models.CharField(max_length=30)
    Description=models.CharField(max_length=100)
    Qte=models.IntegerField(default=0)
    prix=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return self.NomP

    

class Achat(models.Model):
    CodeAchat=models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    matierePremiere = models.ForeignKey(MatierePremiere,on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_achat = models.DateField()
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2)
    montant_total_achat_ht = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    montant_paye = models.DecimalField(decimal_places=2, max_digits=10,default=0)

    def __str__(self):
        return self.matierePremiere.NomP
    
    def montant_reste(self):
        return self.montant_total_achat_ht - self.montant_paye
    
class Client(models.Model):
    Code_Client=models.AutoField(primary_key=True)
    Nom=models.CharField(max_length=30)
    Prenom=models.CharField(max_length=30)
    Adress=models.CharField(max_length=50)


class Reglement_Fournisseur(models.Model):
    ID=models.AutoField(primary_key=True)
    fournisseur=models.ForeignKey(Fournisseur,on_delete=models.CASCADE)
    date_reglement=models.DateField()
    montant_versement=models.DecimalField(max_digits=10,decimal_places=2)

class Centre(models.Model):
    Code=models.AutoField(primary_key=True)
    designation=models.CharField(max_length=100,choices=(('centre1', 'Centre 1'), ('centre2', 'Centre 2'), ('centre3', 'Centre 3')))
    def __str__(self):
        return self.designation
    
class Transfert(models.Model):
    CodeTransfert=models.AutoField(primary_key=True)
    date_transfert=models.DateField()
    centre = models.ForeignKey(Centre,on_delete=models.CASCADE)
    matierePremiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    cout_transfert=models.DecimalField(max_digits=10,decimal_places=2)
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    

class Employe(models.Model):
    CodeE=models.AutoField(primary_key=True)
    centre=models.ForeignKey(Centre,on_delete=models.CASCADE)
    NomE=models.CharField(max_length=100)
    AdrE=models.CharField(max_length=200)
    Email=models.EmailField()
    Tlf=models.IntegerField()
    Salaire=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return self.NomE


class Paiement_Emloyes(models.Model):
    CodePay=models.AutoField(primary_key=True)
    employe=models.ForeignKey(Employe,on_delete=models.CASCADE)
    presence=models.BooleanField()
    salaire_journalier=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    salaire_retenu=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    masrouf=models.DecimalField(max_digits=10,decimal_places=2,default=0)