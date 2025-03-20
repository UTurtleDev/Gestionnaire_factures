# Generated by Django 5.1.7 on 2025-03-19 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affaire_number', models.CharField(db_index=True, max_length=10, unique=True)),
                ('affaire_description', models.TextField(max_length=200)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affaires', to='clients.client')),
            ],
        ),
    ]
