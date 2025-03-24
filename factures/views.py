from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice
from affaires.models import Affaire
from datetime import datetime
from .forms import InvoiceForm


# Create your views here.

def factures(request):
    factures= Invoice.objects.all()
    sorted_factures = sorted(factures, key=lambda facture: facture.invoice_number, reverse=True)
    date = datetime.today().date()
    affaires= Affaire.objects.all()

    for facture in sorted_factures:
        facture.day_late = (date - facture.due_date).days

        # S'assure que client_entity_name est toujours défini
        if facture.client is None and not facture.client_entity_name:
            facture.client_entity_name = "Client supprimé"
            facture.save()

    return render(request, 'pages/factures/factures.html', context={"factures": sorted_factures, "date": date, "affaires": affaires})  

def facture_create(request):
    if request.method == "post":
        form = InvoiceForm(request.POST)
        if form.is_valide():
            form.save()
            return redirect('factures:factures')
    else:
        form = InvoiceForm()
    
    return render(request, 'pages/factures/facture_create_form.html', {'form': form})
        


def facture_detail(request, pk):
    facture_detail = get_object_or_404(Invoice, pk=pk)

    return render(request, 'pages/factures/facture_detail.html', {'facture': facture_detail})