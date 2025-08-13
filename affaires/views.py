from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Affaire 
from .forms import AffaireForm

# Create your views here.
def affaires(request):  
    affaires = Affaire.objects.all()
    sorted_affaires = sorted(affaires, key=lambda affaire: affaire.reste_a_facturer, reverse=True)
    total_facture_affaire = sum(affaire.total_facture_ht for affaire in affaires)

    paginator = Paginator(sorted_affaires, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/affaires/affaires.html', context={"affaires": page_obj, "total_facture_affaire":total_facture_affaire})  

def affaire_detail(request, pk):
    affaire_detail = get_object_or_404(Affaire, pk=pk)
    return render(request, 'pages/affaires/affaire_detail.html', {'affaire': affaire_detail})

def affaire_create(request):
    if request.method == 'POST':
        form = AffaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affaires:affaires')
    else:
        form = AffaireForm()

    return render(request, 'pages/affaires/affaire_create_form.html', {'form': form})

def affaire_update(request, pk):
    affaire = get_object_or_404(Affaire, pk=pk)

    if request.method == 'POST':
        form = AffaireForm(request.POST, instance=affaire)
        if form.is_valid():
            form.save()
            return redirect('affaires:affaires')
    else:
        form = AffaireForm(instance=affaire)

                           
    return render(request, 'pages/affaires/affaire_update_form.html', {'form': form, 'affaire': affaire})