document.addEventListener('DOMContentLoaded', function() {
    const exportButton = document.getElementById('export-button');
    
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            // Show loading state
            const originalText = this.textContent;
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Preparing download...';
            
            // Get the project ID from the data attribute
            const projectId = this.getAttribute('data-project-id');
            
            // Create the export URL
            const exportUrl = `/projects/${projectId}/export`;
            
            // Create a hidden link element
            const downloadLink = document.createElement('a');
            downloadLink.href = exportUrl;
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);
            
            // Click the link to start the download
            downloadLink.click();
            
            // Clean up
            document.body.removeChild(downloadLink);
            
            // Restore button state after a short delay
            setTimeout(() => {
                this.disabled = false;
                this.textContent = originalText;
            }, 2000);
        });
    }
    
    // Show export instructions modal
    const instructionsButton = document.getElementById('export-instructions-button');
    if (instructionsButton) {
        instructionsButton.addEventListener('click', function() {
            const instructionsModal = new bootstrap.Modal(document.getElementById('export-instructions-modal'));
            instructionsModal.show();
        });
    }
    
    // Copy code snippet to clipboard
    const copyButtons = document.querySelectorAll('.copy-snippet');
    if (copyButtons.length > 0) {
        copyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const snippetText = this.closest('.code-snippet-container').querySelector('code').textContent;
                
                // Copy to clipboard
                navigator.clipboard.writeText(snippetText).then(() => {
                    // Update button text temporarily
                    const originalText = this.textContent;
                    this.textContent = 'Copied!';
                    
                    // Restore original text after a delay
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        });
    }
});
