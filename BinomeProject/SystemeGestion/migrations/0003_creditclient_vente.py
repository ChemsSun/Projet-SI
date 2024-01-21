# Generated by Django 5.0 on 2024-01-21 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemeGestion', '0002_alter_paiement_emloyes_masrouf_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant_vente', models.FloatField()),
                ('montant_paye', models.FloatField()),
                ('montant_restant', models.FloatField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.client')),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montant_vente', models.FloatField(editable=False)),
                ('Client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.client')),
                ('credit_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.creditclient')),
                ('mtrP', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemeGestion.matierepremiere')),
            ],
        ),
    ]
