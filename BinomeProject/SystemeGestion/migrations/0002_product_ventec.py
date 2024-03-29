# Generated by Django 5.0 on 2024-01-24 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemeGestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('CodP', models.AutoField(primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=30)),
                ('designation', models.CharField(max_length=30)),
                ('date_production', models.DateField()),
                ('Quantite', models.IntegerField(default=0)),
                ('price_v', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.centre')),
            ],
        ),
        migrations.CreateModel(
            name='VenteC',
            fields=[
                ('CodeVenteC', models.AutoField(primary_key=True, serialize=False)),
                ('qte', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montant_vente', models.FloatField(editable=False)),
                ('Client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.client')),
                ('centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.centre')),
                ('prdt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.product')),
            ],
        ),
    ]
