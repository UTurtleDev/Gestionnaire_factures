/**
 * Client Form JavaScript - Simplified for UX with Django Formsets
 * Focuses on user experience while Django handles validation and backend logic
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form management
    initializeFormManagement();
    
    // Ensure UI consistency for principal contacts
    ensurePrincipalContactUI();
    
    // Initialize client-based contact selection
    initializeExistingContactSelection();
});

/**
 * Initialize dynamic form management
 */
function initializeFormManagement() {
    const addContactBtn = document.getElementById('add-contact');
    if (addContactBtn) {
        addContactBtn.addEventListener('click', addContact);
    }
    
    // Add event listeners to existing principal checkboxes for UI feedback
    document.querySelectorAll('.principal-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handlePrincipalChangeUI);
    });
}

/**
 * Add a new contact form (UI only - Django formset handles backend)
 */
function addContact() {
    const template = document.getElementById('contact-template');
    const container = document.getElementById('contacts-container');
    const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');
    
    if (!template || !container || !totalFormsInput) return;
    
    // Get current form count from Django management form
    const currentIndex = parseInt(totalFormsInput.value);
    
    // Clone the template
    const newContact = template.cloneNode(true);
    newContact.style.display = 'block';
    newContact.id = `contact-${currentIndex}`;
    
    // Update the header
    const header = newContact.querySelector('h4');
    if (header) {
        header.textContent = `Contact ${currentIndex + 1}`;
    }
    
    // Replace __INDEX__ with actual index in all form fields
    const inputs = newContact.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.name) {
            input.name = input.name.replace('__INDEX__', currentIndex);
        }
        if (input.id) {
            input.id = input.id.replace('__INDEX__', currentIndex);
        }
    });
    
    // Add event listener for principal checkbox UI feedback
    const principalCheckbox = newContact.querySelector('.principal-checkbox');
    if (principalCheckbox) {
        principalCheckbox.addEventListener('change', handlePrincipalChangeUI);
    }
    
    // Insert before the template
    container.insertBefore(newContact, template);
    
    // Update Django formset management form
    totalFormsInput.value = currentIndex + 1;
}

/**
 * Remove a contact form (UI feedback - Django handles actual validation)
 */
function removeContact(button) {
    const contactForm = button.closest('.contact-form');
    if (!contactForm) return;
    
    // Check if an existing contact is selected
    const existingContactSelect = document.getElementById('existing-contact-select');
    const hasExistingContact = existingContactSelect && existingContactSelect.value;
    
    // UI check: Don't allow removal if it's the only visible contact AND no existing contact is selected
    const visibleContacts = document.querySelectorAll('.contact-form:not(#contact-template):not([style*="display: none"])');
    if (visibleContacts.length <= 1 && !hasExistingContact) {
        alert('Au moins un contact est requis.');
        return;
    }
    
    // Check if we're removing the principal contact for UI feedback
    const principalCheckbox = contactForm.querySelector('.principal-checkbox');
    const wasPrincipal = principalCheckbox && principalCheckbox.checked;
    
    // Mark for deletion if it has a DELETE field (existing forms)
    const deleteCheckbox = contactForm.querySelector('input[name$="-DELETE"]');
    if (deleteCheckbox) {
        deleteCheckbox.checked = true;
        contactForm.style.display = 'none';
    } else {
        // If no DELETE field, just remove (newly added forms)
        contactForm.remove();
        updateDjangoFormsetIndices();
    }
    
    // UI feedback: If we removed the principal contact, suggest user select another
    if (wasPrincipal) {
        const firstVisibleContact = document.querySelector('.contact-form:not(#contact-template):not([style*="display: none"]) .principal-checkbox');
        if (firstVisibleContact) {
            firstVisibleContact.checked = true;
        }
    }
    
    // After removal, check if we need to hide the first contact remove button again
    const remainingVisibleContacts = document.querySelectorAll('.contact-form:not(#contact-template):not([style*="display: none"])');
    const firstContactRemoveBtn = document.getElementById('first-contact-remove-btn');
    
    if (remainingVisibleContacts.length <= 1 && !hasExistingContact && firstContactRemoveBtn) {
        firstContactRemoveBtn.style.display = 'none';
    }
}

/**
 * Handle principal contact changes for UI feedback only
 * Django backend validation ensures business rules are enforced
 */
function handlePrincipalChangeUI(event) {
    if (event.target.checked) {
        // UI feedback: uncheck other principal checkboxes for better UX
        document.querySelectorAll('.principal-checkbox').forEach(checkbox => {
            if (checkbox !== event.target) {
                checkbox.checked = false;
            }
        });
    }
    // Note: Django backend validation will ensure at least one principal exists
}

/**
 * Ensure UI shows at least one principal contact (visual feedback only)
 * Django formset validation handles the actual business rule enforcement
 */
function ensurePrincipalContactUI() {
    const visiblePrincipalCheckboxes = [];
    document.querySelectorAll('.contact-form:not(#contact-template)').forEach(form => {
        if (form.style.display !== 'none') {
            const checkbox = form.querySelector('.principal-checkbox');
            if (checkbox) {
                visiblePrincipalCheckboxes.push(checkbox);
            }
        }
    });
    
    const checkedPrincipal = visiblePrincipalCheckboxes.filter(cb => cb.checked);
    
    // UI feedback: if no principal is selected, check the first one
    if (checkedPrincipal.length === 0 && visiblePrincipalCheckboxes.length > 0) {
        visiblePrincipalCheckboxes[0].checked = true;
    }
}

/**
 * Update Django formset indices after dynamic changes
 */
function updateDjangoFormsetIndices() {
    const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');
    if (totalFormsInput) {
        const visibleForms = document.querySelectorAll('.contact-form:not(#contact-template)').length;
        totalFormsInput.value = visibleForms;
    }
}

/**
 * Initialize existing contact selection functionality
 */
function initializeExistingContactSelection() {
    console.log('=== DEBUT initializeExistingContactSelection ===');
    
    const clientSelect = document.getElementById('client-select');
    const existingContactSelect = document.getElementById('existing-contact-select');
    const principalCheckbox = document.getElementById('existing-contact-principal');
    
    console.log('Elements trouvés:');
    console.log('- clientSelect:', !!clientSelect, clientSelect?.value);
    console.log('- existingContactSelect:', !!existingContactSelect, existingContactSelect?.value);
    console.log('- principalCheckbox:', !!principalCheckbox, principalCheckbox?.disabled);
    
    if (!clientSelect || !existingContactSelect) {
        console.log('ERREUR: Elements manquants, sortie de la fonction');
        return;
    }
    
    // Initialize the principal checkbox state
    if (principalCheckbox) {
        const shouldDisable = !existingContactSelect.value;
        principalCheckbox.disabled = shouldDisable;
        console.log('Initialisation checkbox principal - disabled:', shouldDisable);
    }
    
    // If client is already selected (update mode), load contacts immediately
    if (clientSelect.value) {
        console.log('Client déjà sélectionné:', clientSelect.value, '- chargement des contacts');
        fetchContactsForClient(clientSelect.value, existingContactSelect);
    }
    
    // Handle client selection change
    clientSelect.addEventListener('change', function() {
        const clientId = this.value;
        console.log('Changement client:', clientId);
        
        if (clientId) {
            // Fetch contacts for this client via AJAX
            fetchContactsForClient(clientId, existingContactSelect);
        } else {
            // Clear the existing contact options
            clearContactOptions(existingContactSelect);
        }
    });
    
    // Handle existing contact selection
    existingContactSelect.addEventListener('change', function() {
        console.log('Changement contact existant:', this.value);
        handleExistingContactSelection(this);
    });
    
    console.log('=== FIN initializeExistingContactSelection ===');
}

/**
 * Fetch contacts for a specific client
 */
function fetchContactsForClient(clientId, selectElement) {
    // Show loading state
    selectElement.innerHTML = '<option value="">Chargement...</option>';
    selectElement.disabled = true;
    
    // Check if we're in update mode by looking for affaire ID in the URL or form
    const currentAffaireId = getCurrentAffaireId();
    let apiUrl = `/affaires/api/client-contacts/${clientId}/`;
    if (currentAffaireId) {
        apiUrl += `?current_affaire_id=${currentAffaireId}`;
    }
    
    // Make AJAX request to get contacts
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            populateContactOptions(selectElement, data.contacts);
            
            // Reset the principal checkbox state after loading contacts
            const principalCheckbox = document.getElementById('existing-contact-principal');
            if (principalCheckbox) {
                principalCheckbox.disabled = true;
                principalCheckbox.checked = false;
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement des contacts:', error);
            selectElement.innerHTML = '<option value="">Erreur de chargement</option>';
        })
        .finally(() => {
            selectElement.disabled = false;
        });
}

/**
 * Get current affaire ID from URL (for update mode)
 */
function getCurrentAffaireId() {
    const urlParts = window.location.pathname.split('/');
    // Look for pattern like /affaires/123/modifier/
    const modifierIndex = urlParts.indexOf('modifier');
    if (modifierIndex > 0 && urlParts[modifierIndex - 1]) {
        return urlParts[modifierIndex - 1];
    }
    return null;
}

/**
 * Populate contact options in the select element
 */
function populateContactOptions(selectElement, contacts) {
    // Clear existing options
    selectElement.innerHTML = '<option value="">Sélectionner un contact existant</option>';
    
    // Add contact options
    contacts.forEach(contact => {
        const option = document.createElement('option');
        option.value = contact.id;
        
        // Build contact display text
        let displayText = `${contact.nom} ${contact.prenom}`;
        if (contact.fonction) {
            displayText += ` - ${contact.fonction}`;
        }
        
        // Mark contacts that are already in this affaire
        if (contact.already_in_affaire) {
            displayText += ' (Déjà dans cette affaire)';
            option.style.color = '#999';
            option.disabled = true;
        }
        
        option.textContent = displayText;
        selectElement.appendChild(option);
    });
}

/**
 * Clear contact options
 */
function clearContactOptions(selectElement) {
    selectElement.innerHTML = '<option value="">Sélectionner d\'abord un client</option>';
    selectElement.disabled = true;
}

/**
 * Handle existing contact selection
 */
function handleExistingContactSelection(selectElement) {
    const contactId = selectElement.value;
    const principalCheckbox = document.getElementById('existing-contact-principal');
    const firstContactRemoveBtn = document.getElementById('first-contact-remove-btn');
    
    console.log('Contact sélectionné:', contactId, 'Principal checkbox trouvée:', !!principalCheckbox);
    
    if (contactId) {
        // Enable the principal checkbox
        if (principalCheckbox) {
            principalCheckbox.disabled = false;
            console.log('Checkbox principal activée');
        }
        
        // Show the remove button for first contact since we have an existing contact selected
        if (firstContactRemoveBtn) {
            firstContactRemoveBtn.style.display = 'block';
        }
        
        // Optional: Provide visual feedback that an existing contact is selected
        const existingSection = selectElement.closest('.existing-contact-section');
        if (existingSection) {
            existingSection.style.backgroundColor = '#e8f5e8';
            existingSection.style.borderColor = '#4CAF50';
        }
        
        // Optional: Show a message to the user
        showContactSelectionMessage('Contact existant sélectionné. Vous pouvez aussi ajouter des contacts supplémentaires ci-dessous.');
    } else {
        // Disable and uncheck the principal checkbox
        if (principalCheckbox) {
            principalCheckbox.disabled = true;
            principalCheckbox.checked = false;
        }
        
        // Hide the remove button for first contact to ensure at least one contact
        if (firstContactRemoveBtn) {
            firstContactRemoveBtn.style.display = 'none';
        }
        
        // Reset visual feedback
        const existingSection = selectElement.closest('.existing-contact-section');
        if (existingSection) {
            existingSection.style.backgroundColor = '#f9f9f9';
            existingSection.style.borderColor = '#e0e0e0';
        }
        
        hideContactSelectionMessage();
    }
}

/**
 * Show contact selection message
 */
function showContactSelectionMessage(message) {
    let messageElement = document.getElementById('contact-selection-message');
    
    if (!messageElement) {
        messageElement = document.createElement('div');
        messageElement.id = 'contact-selection-message';
        messageElement.style.cssText = `
            margin-top: 10px;
            padding: 8px 12px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            color: #155724;
            font-size: 14px;
        `;
        
        const existingSection = document.querySelector('.existing-contact-section');
        if (existingSection) {
            existingSection.appendChild(messageElement);
        }
    }
    
    messageElement.textContent = message;
    messageElement.style.display = 'block';
}

/**
 * Hide contact selection message
 */
function hideContactSelectionMessage() {
    const messageElement = document.getElementById('contact-selection-message');
    if (messageElement) {
        messageElement.style.display = 'none';
    }
}