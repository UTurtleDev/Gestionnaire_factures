from django.shortcuts import render, redirect
from .models import Client
from .forms import ClientForm

# Create your views here.

def clients(request):
    clients = Client.objects.all()
    sorted_clients = sorted(clients, key=lambda client: client.entity_name.lower())

    return render(request, 'pages/clients/clients.html', context={'clients': sorted_clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:clients')
    else:
        form = ClientForm()
    
    return render(request, 'pages/clients/client_create_form.html', {'form': form})