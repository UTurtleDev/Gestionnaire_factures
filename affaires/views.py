from django.shortcuts import render
from .models import Affaire

# Create your views here.
def affaires(request):  
    affaires = Affaire.objects.all()
    total_facture_affaire = sum(affaire.total_facture_ht for affaire in affaires)
    return render(request, 'pages/affaires/affaires.html', context={"affaires": affaires, "total_facture_affaire":total_facture_affaire})  