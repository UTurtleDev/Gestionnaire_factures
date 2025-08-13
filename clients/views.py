from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Client, Contact
from affaires.models import Affaire
from .forms import ClientForm, ContactForm, ContactFormSet

# Create your views here.

def clients(request):
    clients = Client.objects.all()
    sorted_clients = sorted(clients, key=lambda client: client.entity_name.lower())

    paginator = Paginator(sorted_clients,10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/clients/clients.html', context={'clients': page_obj})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        contact_formset = ContactFormSet(request.POST, prefix='contact')
        
        if form.is_valid() and contact_formset.is_valid():
            # Save the client
            client = form.save()
            
            # Process contacts
            for contact_form in contact_formset:
                if contact_form.cleaned_data and not contact_form.cleaned_data.get('DELETE', False):
                    # Skip empty forms
                    if hasattr(contact_form, '_is_empty_form') and contact_form._is_empty_form:
                        continue
                    
                    # Create contact instance
                    contact = contact_form.save(commit=False)
                    contact.client = client
                    contact.save()
            
            return redirect('clients:clients')
    else:
        form = ClientForm()
        contact_formset = ContactFormSet(prefix='contact')
    
    return render(request, 'pages/clients/client_create_form.html', {
        'form': form,
        'contact_formset': contact_formset
    })


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


def contacts(request):
    contacts = Contact.objects.all()
    sorted_contacts = sorted(contacts, key=lambda contact: contact.nom.lower())
    return render(request, 'pages/clients/contacts.html', context={'contacts': sorted_contacts})


def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:contacts')
        
    else:
        form = ContactForm()
    
    return render(request, 'pages/clients/contact_create_form.html', {'form': form})

def contact_detail(request, pk):
    contact_detail = get_object_or_404(Contact, pk=pk)

    return render(request, 'pages/clients/contact_detail.html', {'contact': contact_detail})

def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('clients:contacts')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'pages/clients/contact_update_form.html', {'form': form, 'contact': contact})


def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":
        contact.delete()
        return redirect('clients:contacts')
    
    return redirect('clients:contacts')
    
   