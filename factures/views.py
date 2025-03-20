from django.shortcuts import render
from .models import Invoice
from affaires.models import Affaire
from datetime import datetime


# Create your views here.

def factures(request):
    factures= Invoice.objects.all()
    sorted_factures = sorted(factures, key=lambda facture: facture.invoice_number, reverse=True)
    date = datetime.today().date()
    affaires= Affaire.objects.all()
    for facture in sorted_factures:
        facture.day_late = (date - facture.due_date).days
    return render(request, 'pages/factures.html', context={"factures": sorted_factures, "date": date, "affaires": affaires})  


