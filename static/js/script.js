// Custom JavaScript for the inventory management application

document.addEventListener('DOMContentLoaded', function() {
    // Auto-close alert messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation for movement form
    const movementForm = document.querySelector('#movement-form');
    if (movementForm) {
        movementForm.addEventListener('submit', function(event) {
            const fromLocation = document.querySelector('#from_location').value;
            const toLocation = document.querySelector('#to_location').value;
            
            if (!fromLocation && !toLocation) {
                alert('Either From Location or To Location must be specified');
                event.preventDefault();
                return false;
            }
            
            if (fromLocation && toLocation && fromLocation === toLocation) {
                alert('From Location and To Location cannot be the same');
                event.preventDefault();
                return false;
            }
            
            return true;
        });
    }

    // Dynamic form handling for movement form
    const productSelect = document.querySelector('#product_id');
    const fromLocationSelect = document.querySelector('#from_location');
    const toLocationSelect = document.querySelector('#to_location');
    
    if (productSelect && fromLocationSelect && toLocationSelect) {
        // Add event listeners to check available quantities
        fromLocationSelect.addEventListener('change', function() {
            if (this.value) {
                // Clear to_location if it's the same as from_location
                if (toLocationSelect.value === this.value) {
                    toLocationSelect.value = '';
                }
            }
        });
        
        toLocationSelect.addEventListener('change', function() {
            if (this.value) {
                // Clear from_location if it's the same as to_location
                if (fromLocationSelect.value === this.value) {
                    fromLocationSelect.value = '';
                }
            }
        });
    }

    // Data table initialization
    const dataTables = document.querySelectorAll('.data-table');
    if (dataTables.length > 0) {
        dataTables.forEach(function(table) {
            $(table).DataTable({
                "responsive": true,
                "order": [[0, "desc"]],
                "language": {
                    "search": "Filter:",
                    "paginate": {
                        "next": "Next",
                        "previous": "Prev"
                    }
                }
            });
        });
    }
});