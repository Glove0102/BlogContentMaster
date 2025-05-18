document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Show active tab based on URL hash
    const showTabFromHash = () => {
        const hash = window.location.hash;
        if (hash) {
            const tabEl = document.querySelector(`a[href="${hash}"]`);
            if (tabEl) {
                new bootstrap.Tab(tabEl).show();
            }
        }
    };

    // Show tab on page load
    showTabFromHash();

    // Show tab when hash changes
    window.addEventListener('hashchange', showTabFromHash);

    // Add hash to URL when tab is shown
    document.querySelectorAll('a[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (e) {
            const hash = e.target.getAttribute('href');
            if (hash && hash !== '#') {
                history.replaceState(null, null, hash);
            }
        });
    });

    // File input display
    document.querySelectorAll('.custom-file-input').forEach(fileInput => {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0]?.name || 'No file chosen';
            const fileLabel = this.nextElementSibling;
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
        });
    });

    // Show confirmation modal before delete
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            if (!confirm(this.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });

    // Responsive iframes
    document.querySelectorAll('iframe').forEach(iframe => {
        const wrapper = document.createElement('div');
        wrapper.classList.add('ratio', 'ratio-16x9');
        iframe.parentNode.insertBefore(wrapper, iframe);
        wrapper.appendChild(iframe);
    });
});
