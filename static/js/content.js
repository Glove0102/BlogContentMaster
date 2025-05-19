document.addEventListener('DOMContentLoaded', function() {
    const contentForm = document.getElementById('content-form');
    const topicInput = document.getElementById('topic-input');
    const inspirationUrl = document.getElementById('inspiration-url');
    const titleInput = document.getElementById('title');
    const generateBtn = document.getElementById('generate-btn');
    const previewContainer = document.getElementById('preview-container');
    
    // Function to validate form before submission
    if (contentForm) {
        contentForm.addEventListener('submit', function(e) {
            // Title is now optional - AI will generate if not provided
            
            // Check if either topic or URL is provided
            if (!topicInput.value.trim() && !inspirationUrl.value.trim()) {
                e.preventDefault();
                showValidationError(topicInput, 'Please provide either a topic or an inspiration URL');
                return false;
            }
            
            // Validate URL if provided
            if (inspirationUrl.value.trim() && !isValidUrl(inspirationUrl.value.trim())) {
                e.preventDefault();
                showValidationError(inspirationUrl, 'Please enter a valid URL');
                return false;
            }
            
            // Show loading state
            if (generateBtn) {
                generateBtn.disabled = true;
                generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
            }
        });
    }
    
    // Character counter for meta description
    const metaDescriptionInput = document.getElementById('meta-description');
    const charCounter = document.getElementById('char-counter');
    
    if (metaDescriptionInput && charCounter) {
        metaDescriptionInput.addEventListener('input', function() {
            const remainingChars = 150 - this.value.length;
            charCounter.textContent = remainingChars;
            
            if (remainingChars < 0) {
                charCounter.classList.add('text-danger');
            } else {
                charCounter.classList.remove('text-danger');
            }
        });
        
        // Trigger on page load
        metaDescriptionInput.dispatchEvent(new Event('input'));
    }
    
    // Function to show validation errors
    function showValidationError(inputElement, message) {
        inputElement.classList.add('is-invalid');
        
        // Create or update error message
        let errorElement = inputElement.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('invalid-feedback')) {
            errorElement = document.createElement('div');
            errorElement.classList.add('invalid-feedback');
            inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
        }
        
        errorElement.textContent = message;
        
        // Focus the input
        inputElement.focus();
        
        // Remove error on input
        inputElement.addEventListener('input', function() {
            this.classList.remove('is-invalid');
        }, { once: true });
    }
    
    // Function to validate URLs
    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }
    
    // Toggle between topic input and URL inspiration
    const topicOption = document.getElementById('topic-option');
    const urlOption = document.getElementById('url-option');
    const topicSection = document.getElementById('topic-section');
    const urlSection = document.getElementById('url-section');
    
    if (topicOption && urlOption) {
        topicOption.addEventListener('change', function() {
            if (this.checked) {
                topicSection.classList.remove('d-none');
                urlSection.classList.add('d-none');
                inspirationUrl.value = '';
            }
        });
        
        urlOption.addEventListener('change', function() {
            if (this.checked) {
                urlSection.classList.remove('d-none');
                topicSection.classList.add('d-none');
                topicInput.value = '';
            }
        });
        
        // Set default on page load
        if (topicOption.checked) {
            topicSection.classList.remove('d-none');
            urlSection.classList.add('d-none');
        } else if (urlOption.checked) {
            urlSection.classList.remove('d-none');
            topicSection.classList.add('d-none');
        }
    }
});
