from django.shortcuts import render
from factures.models import Invoice
from affaires.models import Affaire
from datetime import datetime
from utils.charts import generate_revenue_chart, generate_revenue_histogram_chart, generate_cumulative_revenue_chart, get_available_years, get_monthly_revenue_by_year, calculate_monthly_averages

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def dashboard(request):
    current_year = datetime.now().year
    passed_year = datetime.now().year - 1

    
    facturation = Invoice.objects.filter(date__year=current_year)
    total_facturation = sum(facture.amount_ht for facture in facturation)
    formatted_total_facturation = f"{total_facturation:,.2f} €".replace(",", " ").replace(".", ",")

    # Total facture dues N
    factures_dues = [facture for facture in facturation if facture.statut != "payee"]
    factures_dues_sorted = sorted(factures_dues, key=lambda facture: facture.due_date, reverse=False)
    total_factures_dues = f"{sum(facture.amount_ttc for facture in factures_dues):,.2f} €".replace(",", " ").replace(".", ",")

    # Total facture dues cumulé
    total_facturation_cumulee =Invoice.objects.all()
    total_factures_dues_cumule = [facture for facture in total_facturation_cumulee if facture.statut != "payee"]
    total_factures_dues_sorted = sorted(total_factures_dues_cumule, key=lambda facture: facture.due_date, reverse=False)
    total_factures_dues_cumule = f"{sum(facture.amount_ttc for facture in total_factures_dues_cumule):,.2f} €".replace(",", " ").replace(".", ",")


    # Factures en retard N
    factures_retard = [facture for facture in factures_dues if facture.statut == "en_retard"]
    total_factures_retard = f"{sum(facture.amount_ttc for facture in factures_retard):,.2f} €".replace(",", " ").replace(".", ",")

    # Factures en retard N-1
    passed_facturation = Invoice.objects.filter(date__year=passed_year)
    passed_factures_retard = [facture for facture in passed_facturation if facture.statut == "en_retard"]
    total_passed_factures_retard = f"{sum(facture.amount_ttc for facture in passed_factures_retard):,.2f} €".replace(",", " ").replace(".", ",")


    # Total factures en retard cumulé
    factures_retard_cumule = [facture for facture in total_facturation_cumulee if facture.statut == "en_retard"]

    # Affaires en cours
    affaires = Affaire.objects.all()
    affaires_en_cours = [affaire for affaire in affaires if affaire.reste_a_facturer > 0]
    affaires_en_cours_sorted = sorted(affaires_en_cours, key=lambda affaire: affaire.reste_a_facturer, reverse=False)
    total_affaires_en_cours = f"{sum(affaire.reste_a_facturer for affaire in affaires_en_cours):,.2f} €".replace(",", " ").replace(".", ",")



    # Gestion du graphique des chiffres d'affaires
    available_years = get_available_years()
    selected_years = request.GET.getlist('years')
    
    if selected_years:
        selected_years = [int(year) for year in selected_years if year.isdigit()]
    else:
        # Par défaut, sélectionner les deux dernières années disponibles
        selected_years = available_years[:2] if len(available_years) >= 2 else available_years
    
    chart_path = None
    histogram_chart_path = None
    cumulative_chart_path = None
    monthly_averages = None
    if selected_years:
        try:
            chart_path = generate_revenue_chart(selected_years)
            histogram_chart_path = generate_revenue_histogram_chart(selected_years)
            cumulative_chart_path = generate_cumulative_revenue_chart(selected_years)
            
            # Calculer les moyennes mensuelles
            invoices = Invoice.objects.filter(date__year__in=selected_years)
            revenue_data = get_monthly_revenue_by_year(invoices, selected_years)
            monthly_averages = calculate_monthly_averages(revenue_data, selected_years)
        except Exception as e:
            print(f"Erreur lors de la génération du graphique: {e}")

    return render(request, 'pages/dashboard/dashboard.html', {
        'current_year': current_year,
        'passed_year': passed_year,
        'facturation': facturation,
        'total_facturation': total_facturation,
        'total_factures_dues_cumule': total_factures_dues_cumule,
        'factures_dues_sorted': factures_dues_sorted,
        'formatted_total_facturation': formatted_total_facturation,
        'affaires_en_cours': affaires_en_cours_sorted,
        'total_affaires_en_cours': total_affaires_en_cours,
        'factures_dues_sorted': factures_dues_sorted,
        'total_factures_dues': total_factures_dues,
        'factures_retard': factures_retard,
        'total_factures_retard': total_factures_retard,
        'total_passed_factures_retard': total_passed_factures_retard,
        'factures_retard_cumule': factures_retard_cumule,
        'chart_path': chart_path,
        'histogram_chart_path': histogram_chart_path,
        'cumulative_chart_path': cumulative_chart_path,
        'monthly_averages': monthly_averages,
        'available_years': available_years,
        'selected_years': selected_years,
    })




def chiffre_d_affaires(request):
    # Facturation année en cours
    current_year = datetime.now().year
    facturation = Invoice.objects.filter(date__year=current_year)
    total_facturation = sum(facture.amount_ht for facture in facturation)
    formatted_total_facturation = f"{total_facturation:,.2f} €".replace(",", " ").replace(".", ",")
    
    # Facturation année dernière
    passed_year = datetime.now().year - 1
    passed_facturation = Invoice.objects.filter(date__year=passed_year)
    passed_total_facturation = sum(facture.amount_ht for facture in passed_facturation)
    passed_formatted_total_facturation = f"{passed_total_facturation:,.2f} €".replace(",", " ").replace(".", ",")




        # Gestion du graphique des chiffres d'affaires
    available_years = get_available_years()
    selected_years = request.GET.getlist('years')
    
    if selected_years:
        selected_years = [int(year) for year in selected_years if year.isdigit()]
    else:
        # Par défaut, sélectionner les deux dernières années disponibles
        selected_years = available_years[:2] if len(available_years) >= 2 else available_years
    
    chart_path = None
    histogram_chart_path = None
    cumulative_chart_path = None
    monthly_averages = None
    if selected_years:
        try:
            chart_path = generate_revenue_chart(selected_years)
            histogram_chart_path = generate_revenue_histogram_chart(selected_years)
            cumulative_chart_path = generate_cumulative_revenue_chart(selected_years)
            
            # Calculer les moyennes mensuelles
            invoices = Invoice.objects.filter(date__year__in=selected_years)
            revenue_data = get_monthly_revenue_by_year(invoices, selected_years)
            monthly_averages = calculate_monthly_averages(revenue_data, selected_years)
        except Exception as e:
            print(f"Erreur lors de la génération du graphique: {e}")

    return render(request, 'pages/dashboard/chiffre_d_affaires.html', {
        'current_year': current_year,
        'passed_year': passed_year,
        'formatted_total_facturation': formatted_total_facturation,
        'passed_formatted_total_facturation': passed_formatted_total_facturation,
        'chart_path': chart_path,
        'histogram_chart_path': histogram_chart_path,
        'available_years': available_years,
        'cumulative_chart_path': cumulative_chart_path,
        'monthly_averages': monthly_averages,
        'selected_years': selected_years,
    })
