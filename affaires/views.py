from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import ProtectedError
from .models import Affaire 
from .forms import AffaireForm, ContactFormSet, ContactInlineFormSet
from clients.models import Contact

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
    # Ordonner les contacts pour que le contact principal apparaisse en premier
    contacts = affaire_detail.contacts.all().order_by('-is_principal', 'nom', 'prenom')
    contact_principal = affaire_detail.contact_principal
    
    return render(request, 'pages/affaires/affaire_detail.html', {
        'affaire': affaire_detail,
        'contacts': contacts,
        'contact_principal': contact_principal
    })

def affaire_create(request):
    if request.method == 'POST':
        form = AffaireForm(request.POST)
        # Check if existing contact is selected before creating formset
        existing_contact_selected = bool(request.POST.get('existing_contact'))
        contact_formset = ContactFormSet(
            request.POST, 
            prefix='contact',
            existing_contact_selected=existing_contact_selected
        )
        
        if form.is_valid() and contact_formset.is_valid():
            # Save the affaire
            affaire = form.save()
            
            # Handle existing contact selection first
            existing_contact = form.cleaned_data.get('existing_contact')
            existing_contact_is_principal = request.POST.get('existing_contact_is_principal') == 'on'
            
            if existing_contact:
                # Copy the existing contact to this affaire
                Contact.objects.create(
                    affaire=affaire,
                    nom=existing_contact.nom,
                    prenom=existing_contact.prenom,
                    fonction=existing_contact.fonction,
                    phone_number=existing_contact.phone_number,
                    email=existing_contact.email,
                    is_principal=existing_contact_is_principal
                )
            
            # Process new contacts from formset
            has_new_contacts = False
            for contact_form in contact_formset:
                if contact_form.cleaned_data and not contact_form.cleaned_data.get('DELETE', False):
                    # Skip empty forms
                    if hasattr(contact_form, '_is_empty_form') and contact_form._is_empty_form:
                        continue
                    
                    # Create contact instance
                    contact = contact_form.save(commit=False)
                    contact.affaire = affaire
                    # If we already copied an existing contact, new contacts should not be principal by default
                    if existing_contact and not contact.is_principal:
                        contact.is_principal = False
                    contact.save()
                    has_new_contacts = True
            
            # If no existing contact was selected and no new contacts were created,
            # ensure at least one contact exists (this shouldn't happen due to validation)
            if not existing_contact and not has_new_contacts:
                # This case should be handled by form validation
                pass
            
            return redirect('affaires:affaires')
    else:
        form = AffaireForm()
        contact_formset = ContactFormSet(prefix='contact')

    return render(request, 'pages/affaires/affaire_create_form.html', {
        'form': form,
        'contact_formset': contact_formset
    })

def affaire_update(request, pk):
    affaire = get_object_or_404(Affaire, pk=pk)
    
    if request.method == 'POST':
        form = AffaireForm(request.POST, instance=affaire)
        contact_formset = ContactInlineFormSet(request.POST, instance=affaire, prefix='contact')
        
        print(f"=== DEBUG AFFAIRE UPDATE ===")
        print(f"Form valid: {form.is_valid()}")
        print(f"Formset valid: {contact_formset.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        if not contact_formset.is_valid():
            print(f"Formset errors: {contact_formset.errors}")
            
        if form.is_valid() and contact_formset.is_valid():
            # Save the affaire
            form.save()
            
            # Handle existing contact selection
            existing_contact = form.cleaned_data.get('existing_contact')
            existing_contact_is_principal = request.POST.get('existing_contact_is_principal') == 'on'
            
            print(f"Existing contact: {existing_contact}")
            print(f"Is principal: {existing_contact_is_principal}")
            
            if existing_contact:
                print(f"Processing existing contact: {existing_contact.nom} {existing_contact.prenom}")
                
                # Check if this contact already exists for this affaire to avoid duplicates
                existing_contact_for_affaire = Contact.objects.filter(
                    affaire=affaire,
                    nom=existing_contact.nom,
                    prenom=existing_contact.prenom,
                    email=existing_contact.email
                ).first()
                
                print(f"Contact already exists: {existing_contact_for_affaire is not None}")
                
                if not existing_contact_for_affaire:
                    # Copy the existing contact to this affaire only if it doesn't already exist
                    new_contact = Contact.objects.create(
                        affaire=affaire,
                        nom=existing_contact.nom,
                        prenom=existing_contact.prenom,
                        fonction=existing_contact.fonction,
                        phone_number=existing_contact.phone_number,
                        email=existing_contact.email,
                        is_principal=existing_contact_is_principal
                    )
                    print(f"Created new contact: {new_contact.id}")
                elif existing_contact_is_principal:
                    # If contact already exists but we want to make it principal
                    existing_contact_for_affaire.is_principal = True
                    existing_contact_for_affaire.save()
                    print(f"Updated existing contact as principal")
            
            # Save contacts
            contact_formset.save()
            print("=== END DEBUG ===")
            
            return redirect('affaires:affaires')
    else:
        form = AffaireForm(instance=affaire)
        contact_formset = ContactInlineFormSet(instance=affaire, prefix='contact')
                           
    return render(request, 'pages/affaires/affaire_update_form.html', {
        'form': form, 
        'affaire': affaire,
        'contact_formset': contact_formset
    })


def affaire_delete(request, pk):
    affaire = get_object_or_404(Affaire, pk=pk)
    
    if request.method == "POST":
        try:
            affaire_number = affaire.affaire_number  # Sauvegarder pour le message
            affaire.delete()
            messages.success(request, f"L'affaire {affaire_number} a été supprimée avec succès.")
            return redirect('affaires:affaires')
        except ProtectedError:
            messages.error(request, f"Impossible de supprimer l'affaire {affaire.affaire_number} car elle contient des factures ou des paiements. Vous devez d'abord supprimer les éléments liés.")
            return redirect('affaires:affaires')
    
    return redirect('affaires:affaires')


def client_contacts_api(request, client_id):
    """API endpoint to get contacts for a specific client"""
    try:
        # Get the current affaire ID if we're in update mode (optional parameter)
        current_affaire_id = request.GET.get('current_affaire_id')
        
        contacts = Contact.objects.filter(affaire__client_id=client_id).distinct().order_by('nom', 'prenom')
        
        # Si aucun contact pour ce client, retourner tous les contacts
        if not contacts.exists():
            contacts = Contact.objects.all().order_by('nom', 'prenom')
        
        # If we're updating an affaire, exclude contacts that are already in this affaire
        if current_affaire_id:
            try:
                current_affaire_id = int(current_affaire_id)
                # Get contacts that already exist in this affaire to show them differently
                existing_contact_ids = Contact.objects.filter(
                    affaire_id=current_affaire_id
                ).values_list('id', flat=True)
            except (ValueError, TypeError):
                existing_contact_ids = []
        else:
            existing_contact_ids = []
        
        contacts_data = []
        
        for contact in contacts:
            # Mark if this contact is already in the current affaire
            is_already_in_affaire = contact.id in existing_contact_ids if current_affaire_id else False
            
            contacts_data.append({
                'id': contact.id,
                'nom': contact.nom or '',
                'prenom': contact.prenom or '',
                'fonction': contact.fonction or '',
                'phone_number': contact.phone_number or '',
                'email': contact.email or '',
                'is_principal': contact.is_principal,
                'already_in_affaire': is_already_in_affaire
            })
        
        return JsonResponse({'contacts': contacts_data})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)