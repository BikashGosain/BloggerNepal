window.addEventListener('DOMContentLoaded', () => {
    // Auto-close after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.add('fade-out');  // apply fade out CSS
            setTimeout(() => alert.style.display = 'none', 500); // hide after fade
        });
    }, 5000);
});