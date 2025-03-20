# Generated by Django 5.1.7 on 2025-03-20 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affaires', '0002_alter_affaire_options_affaire_budget'),
        ('factures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='affaire',
            name='facture',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='affaires', to='factures.invoice'),
        ),
    ]
