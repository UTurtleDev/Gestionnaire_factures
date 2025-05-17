from django.shortcuts import render
from factures.models import Invoice

# Create your views here.
def login(request):
    return render(request, 'registration/login.html')

def dashboard(request):
    facturation = Invoice.objects.all()
    total_facturation = sum(facture.amount_ht for facture in facturation)
    formatted_total_facturation = f"{total_facturation:.2f} €".replace(".", ",")
    print(total_facturation, formatted_total_facturation)
    return render(request, 'pages/dashboard/dashboard.html', {'facturation': facturation,
                                                            'total_facturation': total_facturation,
                                                            'formatted_total_facturation': formatted_total_facturation})