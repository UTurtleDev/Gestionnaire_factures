from django.shortcuts import render
from .models import Affaire

# Create your views here.
def affaires(request):  
    affaires = Affaire.objects.all()
    print(affaires)
    total_facture_affaire = sum(affaire.total_facture_ht for affaire in affaires)
    for affaire in affaires:
        print(affaire.affaire_number, total_facture_affaire)
    return render(request, 'pages/affaires/affaires.html', context={"affaires": affaires, "total_facture_affaire":total_facture_affaire})  