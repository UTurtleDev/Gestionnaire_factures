from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from factures.models import Invoice
from affaires.models import Affaire
from clients.models import Client, Contact
from datetime import datetime
from utils.charts import generate_revenue_chart, generate_revenue_histogram_chart, generate_cumulative_revenue_chart, get_available_years, get_monthly_revenue_by_year, calculate_monthly_averages
from utils.exports import (
    export_database, export_clients_csv, export_clients_xlsx, 
    export_affaires_csv, export_affaires_xlsx, export_factures_csv, export_factures_xlsx, 
    export_database_csv, export_database_xlsx, export_contacts_csv, export_contacts_xlsx,
    export_reglements_csv, export_reglements_xlsx
)
from users.forms import CustomAuthenticationForm

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
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




@login_required
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


@login_required
def clients(request):
    from django.db.models import Sum, Count
    from clients.models import Client
    from factures.models import Invoice
    
    # Top 5 des meilleurs clients par CA (chiffre d'affaires facturé)
    top_5_clients_ca = []
    clients_with_invoices = Client.objects.filter(affaires__invoices__isnull=False).distinct()
    
    for client in clients_with_invoices:
        total_facture = sum(invoice.amount_ht for invoice in Invoice.objects.filter(affaire__client=client))
        nb_affaires = client.affaires.count()
        
        if total_facture > 0:
            client.total_facture = total_facture
            client.formatted_total_facture = f"{total_facture:,.2f} €".replace(",", " ").replace(".", ",")
            client.nb_affaires = nb_affaires
            top_5_clients_ca.append(client)
    
    # Trier par total facturé décroissant et prendre les 5 premiers
    top_5_clients_ca = sorted(top_5_clients_ca, key=lambda x: x.total_facture, reverse=True)[:5]
    
    # Affaires en cours par client avec détails
    clients_affaires_en_cours = []
    all_clients = Client.objects.all()
    
    for client in all_clients:
        affaires_en_cours = [affaire for affaire in client.affaires.all() if affaire.reste_a_facturer > 0]
        if affaires_en_cours:
            total_reste = sum(affaire.reste_a_facturer for affaire in affaires_en_cours)
            client_data = {
                'client': client,
                'affaires_en_cours': affaires_en_cours,
                'nb_affaires_en_cours': len(affaires_en_cours),
                'total_reste_a_facturer': total_reste,
                'formatted_total_reste': f"{total_reste:,.2f} €".replace(",", " ").replace(".", ",")
            }
            clients_affaires_en_cours.append(client_data)
    
    # Trier par nom de client alphabétique
    clients_affaires_en_cours = sorted(clients_affaires_en_cours, key=lambda x: x['client'].entity_name.lower())
    
    return render(request, 'pages/dashboard/clients.html', {
        'top_5_clients_ca': top_5_clients_ca,
        'clients_affaires_en_cours': clients_affaires_en_cours,
    })


@login_required
def affaires(request):
    from django.db.models import Sum
    from clients.models import Client
    
    # Top 10 des affaires par budget (ordre décroissant)
    top_10_affaires = Affaire.objects.all().order_by('-budget')[:10]
    
    # Top 10 des clients par total d'affaires
    top_10_clients_raw = Client.objects.annotate(
        total_budget=Sum('affaires__budget')
    ).exclude(total_budget=None).order_by('-total_budget')[:10]
    
    # Formatage des montants
    top_10_clients = []
    for client in top_10_clients_raw:
        client.formatted_total_budget = f"{client.total_budget:,.2f} €".replace(",", " ").replace(".", ",")
        top_10_clients.append(client)

    # Affaires en cours
    affaires = Affaire.objects.all()
    affaires_en_cours = [affaire for affaire in affaires if affaire.reste_a_facturer > 0]
    affaires_en_cours_sorted = sorted(affaires_en_cours, key=lambda affaire: affaire.reste_a_facturer, reverse=True)
    total_affaires_en_cours = f"{sum(affaire.reste_a_facturer for affaire in affaires_en_cours):,.2f} €".replace(",", " ").replace(".", ",")


    
    return render(request, 'pages/dashboard/affaires.html', {
        'top_10_affaires': top_10_affaires,
        'top_10_clients': top_10_clients,
        'affaires': affaires,
        'affaires_en_cours': affaires_en_cours_sorted,
        'total_affaires_en_cours': total_affaires_en_cours
    })


@login_required
def search(request):
    query = request.GET.get('search', '').strip()
    context = {'query': query}
    
    if query:
        # Recherche dans les clients
        clients = Client.objects.filter(
            Q(entity_name__icontains=query) | 
            Q(address__icontains=query) |
            Q(affaires__affaire_number__icontains=query) |
            Q(email__icontains=query)
        ).distinct()
        
        # Recherche dans les contacts
        contacts = Contact.objects.filter(
            Q(prenom__icontains=query) |
            Q(nom__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
        
        # Recherche dans les affaires
        affaires = Affaire.objects.filter(
            Q(affaire_number__icontains=query) |
            Q(author__email__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(affaire_description__icontains=query) |
            Q(client_entity_name__icontains=query)
        )
        
        # Recherche dans les factures
        factures = Invoice.objects.filter(
            Q(invoice_number__icontains=query) |
            Q(client_entity_name__icontains=query) |
            Q(invoice_object__icontains=query) |
            Q(affaire__affaire_number__icontains=query)
        )

        # Recherche dans les autheurs  
        factures = Invoice.objects.filter(
            Q(invoice_number__icontains=query) |
            Q(client_entity_name__icontains=query) |
            Q(invoice_object__icontains=query) |
            Q(affaire__affaire_number__icontains=query) |
            Q(author__email__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )
        
        context.update({
            'clients': clients,
            'contacts': contacts,
            'affaires': affaires,
            'factures': factures,
            'has_results': any([clients, contacts, affaires, factures])
        })
    
    return render(request, 'pages/search/search_results.html', context)


@login_required
def export_modal(request):
    """Vue pour gérer les exports via la modale"""
    if request.method == 'POST':
        export_type = request.POST.get('export_type')
        export_format = request.POST.get('export_format')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        
        try:
            # Validation des dates si nécessaires
            if date_debut:
                date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
            if date_fin:
                date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
            
            # Export de la base de données
            if export_type == 'database':
                if export_format == 'sql':
                    return export_database()
                elif export_format == 'csv':
                    return export_database_csv()
                elif export_format == 'xlsx':
                    return export_database_xlsx()
            
            # Export des clients
            elif export_type == 'clients':
                if export_format == 'csv':
                    return export_clients_csv()
                elif export_format == 'xlsx':
                    return export_clients_xlsx()
            
            # Export des contacts
            elif export_type == 'contacts':
                if export_format == 'csv':
                    return export_contacts_csv()
                elif export_format == 'xlsx':
                    return export_contacts_xlsx()
            
            # Export des règlements
            elif export_type == 'reglements':
                if export_format == 'csv':
                    return export_reglements_csv(date_debut, date_fin)
                elif export_format == 'xlsx':
                    return export_reglements_xlsx(date_debut, date_fin)
            
            # Export des affaires
            elif export_type == 'affaires':
                if export_format == 'csv':
                    return export_affaires_csv(date_debut, date_fin)
                elif export_format == 'xlsx':
                    return export_affaires_xlsx(date_debut, date_fin)
            
            # Export des factures
            elif export_type == 'factures':
                if export_format == 'csv':
                    return export_factures_csv(date_debut, date_fin)
                elif export_format == 'xlsx':
                    return export_factures_xlsx(date_debut, date_fin)
            
        except ValueError as e:
            return JsonResponse({'error': 'Format de date invalide'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Erreur lors de l\'export: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


def logout_view(request):
    logout(request)
    # messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('dashboard:login')

