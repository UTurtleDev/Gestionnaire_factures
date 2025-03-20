from django.shortcuts import render
from .models import Affaire

# Create your views here.
def affaires(request):  
    affaires = Affaire.objects.all()
    return render(request, 'pages/affaires.html', context={"affaires": affaires})  