from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from affaires.models import Affaire
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


def client_detail(request, pk):
    client_detail = get_object_or_404(Client, pk=pk)
    contact = client_detail.contacts.all()
    contact_principal = client_detail.contact_principal



    return render(request, 'pages/clients/client_detail.html', {'client': client_detail, 'contact': contact, 'contact_principal': contact_principal})


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:clients')
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'pages/clients/client_update_form.html', {'form': form, 'client': client})


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        return redirect('clients:clients')
    
    return redirect('clients:clients')

