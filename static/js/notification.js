document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const filterTabs = document.querySelectorAll('.filter-tab');
    const notificationCards = document.querySelectorAll('.notification-card');

    filterTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            filterTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            // Filter notifications
            notificationCards.forEach(card => {
                const status = card.getAttribute('data-status');
                
                if (filter === 'all') {
                    card.style.display = 'flex';
                } else if (filter === 'unread' && status === 'unread') {
                    card.style.display = 'flex';
                } else if (filter === 'read' && status === 'read') {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Smooth scroll on page load if notification param exists
    const urlParams = new URLSearchParams(window.location.search);
    const notificationId = urlParams.get('notification');
    
    if (notificationId) {
        // Find the notification card and scroll to it
        setTimeout(() => {
            const cards = document.querySelectorAll('.notification-card');
            cards.forEach(card => {
                const forms = card.querySelectorAll('form');
                forms.forEach(form => {
                    const input = form.querySelector('button[name="mark_read"]');
                    if (input && input.value === notificationId) {
                        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        card.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.3)';
                        setTimeout(() => {
                            card.style.boxShadow = '';
                        }, 2000);
                    }
                });
            });
        }, 300);
    }
});