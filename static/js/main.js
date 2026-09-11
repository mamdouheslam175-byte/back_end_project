// DevPulse Blog interactive utilities

document.addEventListener('DOMContentLoaded', () => {
    // 1. Share Link button on post detail page
    const copyBtn = document.getElementById('copy-link-btn');
    const copyBtnText = document.getElementById('copy-btn-text');

    if (copyBtn && copyBtnText) {
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(window.location.href);
                const originalText = copyBtnText.textContent;
                copyBtnText.textContent = 'Link Copied! ✓';
                copyBtn.style.borderColor = 'var(--accent-emerald)';
                copyBtn.style.color = 'var(--accent-emerald)';

                setTimeout(() => {
                    copyBtnText.textContent = originalText;
                    copyBtn.style.borderColor = '';
                    copyBtn.style.color = '';
                }, 2200);
            } catch (err) {
                console.error('Failed to copy URL to clipboard:', err);
            }
        });
    }

    // 2. Keyboard shortcut: Press '/' to focus global search bar
    const searchInput = document.getElementById('search-input');
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
            e.preventDefault();
            searchInput?.focus();
        }
    });
});
