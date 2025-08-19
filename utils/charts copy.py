import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour serveur
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict
from django.conf import settings
import os


# Comparatif des chiffres d'affaires mensuels
def get_monthly_revenue_by_year(invoices, years):
    """
    Agrège les chiffres d'affaires mensuels par année
    """
    revenue_data = defaultdict(lambda: defaultdict(float))
    
    for invoice in invoices:
        year = invoice.date.year
        if year in years:
            month = invoice.date.month
            revenue_data[year][month] += float(invoice.amount_ht)
    
    return dict(revenue_data)


def create_revenue_chart(revenue_data, years, output_path):
    """
    Génère un graphique linéaire des chiffres d'affaires avec matplotlib
    """
    plt.figure(figsize=(10, 5))
    plt.style.use('default')
    
    months = list(range(1, 13))
    month_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    
    colors = ['#7FAEDC', '#4ECDC4', '#338ce6', '#FF6B6B', '#45B7D1']
    
    for i, year in enumerate(sorted(years)):
        monthly_values = []
        for month in months:
            monthly_values.append(revenue_data.get(year, {}).get(month, 0))
        
        plt.plot(months, monthly_values, 
                marker='o', 
                linewidth=2.5, 
                markersize=6,
                color=colors[i % len(colors)],
                label=f'{year}')
    
    plt.title('Évolution du chiffre d\'affaires mensuel', fontsize=16, fontweight='bold', pad=20)
    # plt.xlabel('Mois', fontsize=12)
    # plt.ylabel('Chiffre d\'affaires (€)', fontsize=12)
    plt.xticks(months, month_labels)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    # Formatage de l'axe Y avec des milliers séparés
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}€'.replace(',', ' ')))
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_revenue_chart(years=None):
    """
    Fonction principale pour générer le graphique des revenus
    """
    if years is None:
        years = [2024, 2025]
    
    # Import local pour éviter les problèmes de circularité
    from factures.models import Invoice
    
    invoices = Invoice.objects.filter(date__year__in=years)
    revenue_data = get_monthly_revenue_by_year(invoices, years)
    
    # Utiliser le répertoire MEDIA pour les fichiers générés dynamiquement
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    output_filename = f"revenue_chart_{'_'.join(map(str, sorted(years)))}.png"
    output_path = os.path.join(charts_dir, output_filename)
    
    create_revenue_chart(revenue_data, years, output_path)
    
    # Retourner le chemin relatif pour le template avec MEDIA_URL
    return f'charts/{output_filename}'



# Comparatif des chiffres d'affaires cumulés
def get_cumulative_monthly_revenue_by_year(invoices, years):
    """
    Calcule les chiffres d'affaires cumulés mensuels par année
    """
    revenue_data = defaultdict(lambda: defaultdict(float))
    
    for invoice in invoices:
        year = invoice.date.year
        if year in years:
            month = invoice.date.month
            revenue_data[year][month] += float(invoice.amount_ht)
    
    # Calculer les valeurs cumulées
    cumulative_data = defaultdict(lambda: defaultdict(float))
    for year in years:
        cumulative_total = 0
        for month in range(1, 13):
            cumulative_total += revenue_data[year].get(month, 0)
            cumulative_data[year][month] = cumulative_total
    
    return dict(cumulative_data)


def create_cumulative_revenue_chart(cumulative_data, years, output_path):
    """
    Génère un graphique linéaire des chiffres d'affaires cumulés avec matplotlib
    """
    plt.figure(figsize=(10, 5))
    plt.style.use('default')
    
    months = list(range(1, 13))
    month_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                   'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    
    colors = ['#7FAEDC', '#4ECDC4', '#338ce6', '#FF6B6B', '#45B7D1']
    
    for i, year in enumerate(sorted(years)):
        cumulative_values = []
        for month in months:
            cumulative_values.append(cumulative_data.get(year, {}).get(month, 0))
        
        plt.plot(months, cumulative_values, 
                marker='o', 
                linewidth=2.5, 
                markersize=6,
                color=colors[i % len(colors)],
                label=f'{year}')
    
    plt.title('Évolution du chiffre d\'affaires cumulé', fontsize=16, fontweight='bold', pad=20)
    # plt.xlabel('Mois', fontsize=12)
    # plt.ylabel('Chiffre d\'affaires cumulé (€)', fontsize=12)
    plt.xticks(months, month_labels)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    # Formatage de l'axe Y avec des milliers séparés
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}€'.replace(',', ' ')))
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_cumulative_revenue_chart(years=None):
    """
    Fonction principale pour générer le graphique des revenus cumulés
    """
    if years is None:
        years = [2024, 2025]
    
    # Import local pour éviter les problèmes de circularité
    from factures.models import Invoice
    
    invoices = Invoice.objects.filter(date__year__in=years)
    cumulative_data = get_cumulative_monthly_revenue_by_year(invoices, years)
    
    # Utiliser le répertoire MEDIA pour les fichiers générés dynamiquement
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    output_filename = f"cumulative_revenue_chart_{'_'.join(map(str, sorted(years)))}.png"
    output_path = os.path.join(charts_dir, output_filename)
    
    create_cumulative_revenue_chart(cumulative_data, years, output_path)
    
    # Retourner le chemin relatif pour le template avec MEDIA_URL
    return f'charts/{output_filename}'


def get_available_years():
    """
    Récupère toutes les années disponibles dans les factures
    """
    from factures.models import Invoice
    
    years = Invoice.objects.dates('date', 'year').values_list('date__year', flat=True)
    return sorted(set(years), reverse=True)