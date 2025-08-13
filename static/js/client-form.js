/**
 * Client Form JavaScript - Simplified for UX with Django Formsets
 * Focuses on user experience while Django handles validation and backend logic
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form management
    initializeFormManagement();
    
    // Ensure UI consistency for principal contacts
    ensurePrincipalContactUI();
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
    
    // UI check: Don't allow removal if it's the only visible contact
    const visibleContacts = document.querySelectorAll('.contact-form:not(#contact-template):not([style*="display: none"])');
    if (visibleContacts.length <= 1) {
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