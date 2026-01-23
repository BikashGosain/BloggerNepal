    document.addEventListener('DOMContentLoaded', function() {
        // Add click animation to blog cards
        const blogCards = document.querySelectorAll('.blog-card');
        
        blogCards.forEach(card => {
            card.addEventListener('click', function(e) {
                // Don't trigger if clicking on action buttons
                if (!e.target.closest('.blog-actions')) {
                    const link = this.querySelector('.blog-title a');
                    if (link) {
                        window.location.href = link.href;
                    }
                }
            });
        });

        // Add loading animation
        const blogItems = document.querySelectorAll('.blog-item');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                }
            });
        }, { threshold: 0.1 });

        blogItems.forEach(item => {
            observer.observe(item);
        });

        // Delete confirmation with custom styling
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const postTitle = this.closest('.blog-card').querySelector('.blog-title a').textContent.trim();
                
                if (confirm(`Are you sure you want to delete "${postTitle}"?\n\nThis action cannot be undone.`)) {
                    window.location.href = this.href;
                }
            });
        });

        // Add ripple effect on action buttons
        document.querySelectorAll('.action-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });

        // Hover effect for stat badges
        document.querySelectorAll('.stat-badge').forEach(badge => {
            badge.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.05)';
            });
            
            badge.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    });