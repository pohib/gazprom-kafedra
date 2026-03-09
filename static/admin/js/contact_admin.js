(function() {
    'use strict';

    function toggleFields(row) {
        const typeSelect = row.querySelector('select[name*="contact_type"]');
        const labelContainer = row.querySelector('.field-label');
        const urlContainer = row.querySelector('.field-url');

        if (!typeSelect || !labelContainer || !urlContainer) return;

        const val = typeSelect.value;

        if (val === 'text') {
            urlContainer.style.display = 'none';
            labelContainer.style.display = '';
        } else if (val === 'link') {
            urlContainer.style.display = '';
            labelContainer.style.display = 'none';
        } else {
            urlContainer.style.display = '';
            labelContainer.style.display = '';
        }
    }

    window.addEventListener('load', function() {
        const rows = document.querySelectorAll('.dynamic-contacts_set, [id^="contacts_set-"]');
        rows.forEach(row => {
            if (row.tagName === 'TR' || row.classList.contains('inline-related')) {
                toggleFields(row);
            }
        });

        document.addEventListener('change', function(e) {
            if (e.target && e.target.name && e.target.name.includes('contact_type')) {
                const row = e.target.closest('tr') || e.target.closest('.inline-related');
                if (row) toggleFields(row);
            }
        });

        const targetNode = document.querySelector('#contacts_set-group');
        if (targetNode) {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1 && (node.classList.contains('dynamic-contacts_set') || node.tagName === 'TR')) {
                            toggleFields(node);
                        }
                    });
                });
            });
            observer.observe(targetNode, { childList: true, subtree: true });
        }
    });
})();