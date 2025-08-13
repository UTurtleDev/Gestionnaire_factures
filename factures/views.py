from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Invoice, Payment
from affaires.models import Affaire
from datetime import datetime
from .forms import InvoiceForm, PaymentForm


# Create your views here.

def factures(request):
    factures= Invoice.objects.all()
    sorted_factures = sorted(factures, key=lambda facture: facture.invoice_number, reverse=True)
    date = datetime.today().date()
    affaires= Affaire.objects.all()

    paginator = Paginator(sorted_factures, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for facture in sorted_factures:
        facture.day_late = (date - facture.due_date).days

        # S'assure que client_entity_name est toujours défini
        if facture.client is None and not facture.client_entity_name:
            facture.client_entity_name = "Client supprimé"
            facture.save()

    # return render(request, 'pages/factures/factures.html', context={"factures": sorted_factures, "date": date, "affaires": affaires})  
    return render(request, 'pages/factures/factures.html', context={"factures": page_obj, "date": date, "affaires": affaires})  

def facture_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('factures:factures')
    else:
        form = InvoiceForm(initial={'type': 'facture', 'date': datetime.today().strftime('%Y-%m-%d'), 'vat_rate': 20.00})
           
    return render(request, 'pages/factures/facture_create_form.html', {'form': form})

def facture_detail(request, pk):
    facture_detail = get_object_or_404(Invoice, pk=pk)

    return render(request, 'pages/factures/facture_detail.html', {'facture': facture_detail})

def facture_update(request, pk):
    facture = get_object_or_404(Invoice, pk=pk)
    facture.date = facture.date.strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            return redirect('factures:factures')
    else:
        form = InvoiceForm(instance=facture)
    
    return render(request, 'pages/factures/facture_update_form.html', {'form': form, 'facture': facture})

def facture_delete(request, pk):
    facture = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        facture.delete()
        return redirect('factures:factures')
   
def reglements(request):
    paiements = Payment.objects.all()
    factures = Invoice.objects.all()

    for facture in factures:
        if facture.client is None and not facture.client_entity_name:
            facture.client_entity_name = "Client supprimé"
            facture.save()

    return render(request, 'pages/factures/paiements.html', {'paiements': paiements, 'factures': factures})

def reglement_create(request, pk):
    facture = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.invoice = facture  # Assigne la facture au paiement
            paiement.save()
            return redirect('factures:reglements')
    else:
        form = PaymentForm(initial={
            'date': datetime.today().strftime('%Y-%m-%d'), 
            'amount': round(facture.amount_ttc, 2), 
            'payment_method': 'VRT',
            'invoice': facture
            })
    
    return render(request, 'pages/factures/paiement_create_form.html', {'form': form, 'facture': facture})

def reglement_detail(request, pk):
    paiement_detail = get_object_or_404(Payment, pk=pk)
    return render(request, 'pages/factures/paiement_detail.html', {'paiement': paiement_detail})

def reglement_update(request, pk):
    # Récupère le paiement existant à partir de son ID
    paiement = get_object_or_404(Payment, pk=pk)
    facture = paiement.invoice  # Récupère la facture associée au paiement
    paiement.date = paiement.date.strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=paiement)  # Utilise l'instance existante
        if form.is_valid():
            form.save()  # Sauvegarde les modifications
            return redirect('factures:reglements')
        else:
            print("Erreurs de formulaire:", form.errors)
    else:
        # Initialise le formulaire avec les données du paiement existant
        # Convertis la date au format string pour l'affichage
        form = PaymentForm(instance=paiement)
        
        # # Si tu utilises le format de date pour le widget DateInput
        # if isinstance(form.initial.get('date'), datetime.date):
            # form.initial['date'] = form.initial['date'].strftime('%Y-%m-%d')
    
    return render(request, 'pages/factures/paiement_update_form.html', {
        'form': form, 
        'facture': facture,
        'paiement': paiement
    })

def reglement_delete(request, pk):
    paiement = get_object_or_404(Payment, pk=pk)
    facture  = paiement.invoice  # Récupère la facture associée au paiement  

    if request.method == 'POST':
        paiement.delete()
        facture.update_statut() # Mise à jour du statut de la facture
        return redirect('factures:reglements')    

    return redirect('factures:reglements') 

    
    
