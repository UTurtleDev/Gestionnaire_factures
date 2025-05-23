from django.shortcuts import render
from factures.models import Invoice
from affaires.models import Affaire

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def dashboard(request):
    facturation = Invoice.objects.all()
    total_facturation = sum(facture.amount_ht for facture in facturation)
    formatted_total_facturation = f"{total_facturation:,.2f} €".replace(",", " ").replace(".", ",")

    affaires = Affaire.objects.all()
    affaires_en_cours = [affaire for affaire in affaires if affaire.reste_a_facturer > 0]
    affaires_en_cours_sorted = sorted(affaires_en_cours, key=lambda affaire: affaire.reste_a_facturer, reverse=False)
    total_affaires_en_cours = f"{sum(affaire.reste_a_facturer for affaire in affaires_en_cours):,.2f} €".replace(",", " ").replace(".", ",")


    factures_dues = [facture for facture in facturation if facture.statut != "payee"]
    factures_dues_sorted = sorted(factures_dues, key=lambda facture: facture.due_date, reverse=False)
    total_factures_dues = f"{sum(facture.amount_ttc for facture in factures_dues):,.2f} €".replace(",", " ").replace(".", ",")

    factures_retard = [facture for facture in factures_dues if facture.statut == "en_retard"]
    total_factures_retard = f"{sum(facture.amount_ttc for facture in factures_retard):,.2f} €".replace(",", " ").replace(".", ",")

    return render(request, 'pages/dashboard/dashboard.html', {'facturation': facturation,
                                                            'total_facturation': total_facturation,
                                                            'formatted_total_facturation': formatted_total_facturation,
                                                            'affaires_en_cours': affaires_en_cours_sorted,
                                                            'total_affaires_en_cours': total_affaires_en_cours,
                                                            'factures_dues_sorted': factures_dues_sorted,
                                                            'total_factures_dues': total_factures_dues,
                                                            'factures_retard': factures_retard,
                                                            'total_factures_retard': total_factures_retard})