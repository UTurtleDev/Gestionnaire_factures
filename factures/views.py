from django.shortcuts import render
from .models import Invoice
from datetime import datetime

# Create your views here.

def factures(request):
    factures= Invoice.objects.all()
    sorted_factures = sorted(factures, key=lambda facture: facture.invoice_number, reverse=True)
    date = datetime.today().date()
    return render(request, 'pages/factures.html', context={"factures": sorted_factures, "date": date})
