document.addEventListener('DOMContentLoaded', function() {
    // File upload validation
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const htmlFile = document.getElementById('html-file').files[0];
            const cssFile = document.getElementById('css-file').files[0];
            const websitePurpose = document.getElementById('website-purpose').value.trim();
            
            if (!htmlFile || !cssFile) {
                e.preventDefault();
                showAlert('Both HTML and CSS files are required.', 'danger');
                return false;
            }
            
            if (!websitePurpose) {
                e.preventDefault();
                showAlert('Please provide a description of your website\'s purpose.', 'danger');
                return false;
            }
            
            // Check file types
            const htmlExtension = htmlFile.name.split('.').pop().toLowerCase();
            const cssExtension = cssFile.name.split('.').pop().toLowerCase();
            
            if (htmlExtension !== 'html' && htmlExtension !== 'htm') {
                e.preventDefault();
                showAlert('Please upload a valid HTML file.', 'danger');
                return false;
            }
            
            if (cssExtension !== 'css') {
                e.preventDefault();
                showAlert('Please upload a valid CSS file.', 'danger');
                return false;
            }
            
            // Show loading state
            document.getElementById('upload-btn').disabled = true;
            document.getElementById('upload-btn').innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...';
        });
    }
    
    // Project deletion confirmation
    const deleteProjectBtn = document.getElementById('delete-project');
    if (deleteProjectBtn) {
        deleteProjectBtn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    }
    
    // Function to show alerts
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            const alertElement = document.createElement('div');
            alertElement.className = `alert alert-${type} alert-dismissible fade show`;
            alertElement.role = 'alert';
            alertElement.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            
            alertContainer.appendChild(alertElement);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                alertElement.classList.remove('show');
                setTimeout(() => {
                    alertContainer.removeChild(alertElement);
                }, 150);
            }, 5000);
        }
    }
    
    // Initialize file input labels
    const updateFileLabel = (fileInput) => {
        const label = fileInput.nextElementSibling;
        if (fileInput.files.length > 0) {
            label.textContent = fileInput.files[0].name;
        } else {
            label.textContent = label.dataset.default || 'Choose file';
        }
    };
    
    document.querySelectorAll('.custom-file-input').forEach(input => {
        input.addEventListener('change', function() {
            updateFileLabel(this);
        });
        
        // Initialize on page load
        updateFileLabel(input);
    });
});
