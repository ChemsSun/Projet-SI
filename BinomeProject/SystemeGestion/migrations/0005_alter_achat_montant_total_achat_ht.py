# Generated by Django 5.0 on 2024-01-07 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemeGestion', '0004_alter_fournisseur_solde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat',
            name='montant_total_achat_ht',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]