from django.shortcuts import render
from .models import Client

# Create your views here.

def clients(request):
    clients = Client.objects.all()
    sorted_clients = sorted(clients, key=lambda client: client.entity_name.lower())

    return render(request, 'pages/clients.html', context={'clients': sorted_clients})