from django.shortcuts import render, get_object_or_404
from .models import Affaire

# Create your views here.
def affaires(request):  
    affaires = Affaire.objects.all()
    sorted_affaires = sorted(affaires, key=lambda affaire: affaire.reste_a_facturer, reverse=True)
    total_facture_affaire = sum(affaire.total_facture_ht for affaire in affaires)
    return render(request, 'pages/affaires/affaires.html', context={"affaires": sorted_affaires, "total_facture_affaire":total_facture_affaire})  

def affaire_detail(request, pk):
    affaire_detail = get_object_or_404(Affaire, pk=pk)
    return render(request, 'pages/affaires/affaire_detail.html', {'affaire': affaire_detail})