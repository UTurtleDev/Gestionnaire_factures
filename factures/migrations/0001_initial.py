# Generated by Django 5.1.6 on 2025-03-13 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('facture', 'Facture'), ('proforma', 'Proforma'), ('avoir', 'Avoir')], default='facture', max_length=10)),
                ('invoice_number', models.CharField(max_length=10, unique=True)),
                ('invoice_object', models.TextField(max_length=200)),
                ('amount_ht', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vat_rate', models.DecimalField(decimal_places=2, default=20.0, max_digits=5)),
                ('statut', models.CharField(choices=[('a_payer', 'À payer'), ('partiellement_payee', 'Partiellement payée'), ('payee', 'Payée'), ('en_retard', 'En retard'), ('annulee', 'Annulée')], default='a_payer', max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='clients.client')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(max_length=200)),
                ('author', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='factures.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='factures.invoice')),
            ],
        ),
    ]
