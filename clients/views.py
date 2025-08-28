from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Client, Contact
from affaires.models import Affaire
from .forms import ClientForm, ContactAffaireForm, ContactFormSet

# Create your views here.

@login_required
def clients(request):
    clients = Client.objects.all()
    sorted_clients = sorted(clients, key=lambda client: client.entity_name.lower())

    paginator = Paginator(sorted_clients,10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/clients/clients.html', context={'clients': page_obj})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        contact_formset = ContactFormSet(request.POST)
        
        if form.is_valid() and contact_formset.is_valid():
            client = form.save()
            
            # Process contacts - they need to be linked to an affaire
            contacts_to_create = []
            for contact_form in contact_formset:
                if contact_form.cleaned_data and not hasattr(contact_form, '_is_empty_form'):
                    contacts_to_create.append(contact_form.cleaned_data)
            
            # If there are contacts to create, we need an affaire
            if contacts_to_create:
                # Create a default affaire for this client
                from affaires.models import Affaire
                from users.models import CustomUser
                
                # Get the first author user or current user
                default_author = request.user if hasattr(request.user, 'affaires') else CustomUser.objects.filter(is_superuser=True).first()
                
                if default_author:
                    # Generate a unique affaire number
                    from django.utils import timezone
                    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                    affaire_number = f"AFF-{client.pk:03d}-{timestamp}"
                    
                    affaire = Affaire.objects.create(
                        client=client,
                        author=default_author,
                        affaire_number=affaire_number,
                        budget=0.0,
                        affaire_description=f"Affaire par défaut pour {client.entity_name}"
                    )
                    
                    # Create all contacts linked to this affaire
                    for contact_data in contacts_to_create:
                        Contact.objects.create(
                            affaire=affaire,
                            nom=contact_data.get('nom', ''),
                            prenom=contact_data.get('prenom', ''),
                            fonction=contact_data.get('fonction', ''),
                            phone_number=contact_data.get('phone_number', ''),
                            email=contact_data.get('email', ''),
                            is_principal=contact_data.get('is_principal', False)
                        )
            
            messages.success(request, f'Client "{client.entity_name}" créé avec succès.')
            return redirect('clients:clients')
    else:
        form = ClientForm()
        contact_formset = ContactFormSet()
    
    return render(request, 'pages/clients/client_create_form.html', {
        'form': form,
        'contact_formset': contact_formset,
    })


@login_required
def client_detail(request, pk):
    client_detail = get_object_or_404(Client, pk=pk)
    # Les contacts sont maintenant liés aux affaires
    all_contacts = client_detail.tous_les_contacts
    contact_principal = client_detail.contact_principal
    affaires = client_detail.affaires.all()

    return render(request, 'pages/clients/client_detail.html', {
        'client': client_detail, 
        'contact': all_contacts, 
        'contact_principal': contact_principal,
        'affaires': affaires
    })


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    # Get all contacts for this client through their affaires
    client_contacts = client.tous_les_contacts
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        contact_formset = ContactFormSet(request.POST)
        
        if form.is_valid() and contact_formset.is_valid():
            client = form.save()
            
            # Only handle new contacts (non-empty forms)
            new_contacts_added = False
            for contact_form in contact_formset:
                if contact_form.cleaned_data and not hasattr(contact_form, '_is_empty_form'):
                    # This is a new contact to add
                    contact_data = contact_form.cleaned_data
                    
                    # We need to assign to an affaire - use first affaire or create one
                    if not client.affaires.exists():
                        # Create a default affaire for this client if none exists
                        from affaires.models import Affaire
                        from users.models import CustomUser
                        default_author = CustomUser.objects.filter(is_author=True).first()
                        if default_author:
                            affaire = Affaire.objects.create(
                                client=client,
                                author=default_author,
                                affaire_number=f"AFF-{client.pk}-001",
                                budget=0.0,
                                affaire_description=f"Affaire par défaut pour {client.entity_name}"
                            )
                        else:
                            # Skip saving if no author available
                            continue
                    else:
                        affaire = client.affaires.first()
                    
                    # Create contact with affaire
                    Contact.objects.create(
                        affaire=affaire,
                        nom=contact_data.get('nom', ''),
                        prenom=contact_data.get('prenom', ''),
                        fonction=contact_data.get('fonction', ''),
                        phone_number=contact_data.get('phone_number', ''),
                        email=contact_data.get('email', ''),
                        is_principal=contact_data.get('is_principal', False)
                    )
                    new_contacts_added = True
            
            return redirect('clients:clients')
    else:
        form = ClientForm(instance=client)
        
        # Initialize empty formset for new contacts only
        contact_formset = ContactFormSet()
    
    return render(request, 'pages/clients/client_update_form.html', {
        'form': form, 
        'client': client,
        'contact_formset': contact_formset,
        'existing_contacts': client_contacts,  # Pass existing contacts separately
    })


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        try:
            client_name = client.entity_name  # Sauvegarder pour le message
            client.delete()
            messages.success(request, f"Le client {client_name} a été supprimé avec succès.")
            return redirect('clients:clients')
        except ProtectedError:
            messages.error(request, f"Impossible de supprimer le client {client.entity_name} car il est lié à des affaires, factures ou autres éléments. Vous devez d'abord supprimer les éléments liés.")
            return redirect('clients:clients')
    
    return redirect('clients:clients')


@login_required
def contacts(request):
    contacts = Contact.objects.all()
    # Tri sécurisé qui gère les cas où nom peut être None
    sorted_contacts = sorted(contacts, key=lambda contact: (contact.nom or '').lower())

    paginator = Paginator(sorted_contacts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/clients/contacts.html', context={'contacts': page_obj})


@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactAffaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:contacts')
        
    else:
        form = ContactAffaireForm()
    
    return render(request, 'pages/clients/contact_create_form.html', {'form': form})

@login_required
def contact_detail(request, pk):
    contact_detail = get_object_or_404(Contact, pk=pk)

    return render(request, 'pages/clients/contact_detail.html', {'contact': contact_detail})

@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        form = ContactAffaireForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('clients:contacts')
    else:
        form = ContactAffaireForm(instance=contact)
    
    return render(request, 'pages/clients/contact_update_form.html', {'form': form, 'contact': contact})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == "POST":
        contact.delete()
        return redirect('clients:contacts')
    
    return redirect('clients:contacts')
    
   