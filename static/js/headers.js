document.addEventListener('DOMContentLoaded', function() {
    // ===== MOBILE MENU TOGGLE =====
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.textContent = mobileMenu.classList.contains('active') ? '✕' : '☰';
        });
    }

    // ===== DESKTOP DROPDOWN =====
    const navDropdowns = document.querySelectorAll('.nav-dropdown');
    
    navDropdowns.forEach(function(dropdown) {
        const btn = dropdown.querySelector('.nav-dropdown-btn');
        
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Close other dropdowns
            navDropdowns.forEach(function(other) {
                if (other !== dropdown) {
                    other.classList.remove('open');
                }
            });
            
            // Toggle current
            dropdown.classList.toggle('open');
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-dropdown')) {
            navDropdowns.forEach(function(dropdown) {
                dropdown.classList.remove('open');
            });
        }
    });

    // ===== ACTIVE LINK HIGHLIGHTING =====
    const currentPath = window.location.pathname;
    const allNavLinks = document.querySelectorAll('.nav-link');
    
    // Highlight main navigation links
    allNavLinks.forEach(function(link) {
        const linkPath = link.getAttribute('href');
        
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });

    // ===== ACTIVE STATE FOR DESKTOP DROPDOWN ITEMS =====
    navDropdowns.forEach(function(dropdown) {
        const dropdownLinks = dropdown.querySelectorAll('.nav-dropdown-menu a');
        let isActive = false;
        
        dropdownLinks.forEach(function(link) {
            const linkPath = link.getAttribute('href');
            
            if (linkPath === currentPath) {
                link.classList.add('active');
                isActive = true;
            }
        });
        
        // Highlight dropdown button if any link inside is active
        if (isActive) {
            const btn = dropdown.querySelector('.nav-dropdown-btn');
            btn.classList.add('active');
        }
    });

    // ===== ACTIVE STATE FOR MOBILE DETAILS (Categories & Social Links) =====
    const mobileDetails = document.querySelectorAll('.mobile-menu nav details');
    
    mobileDetails.forEach(function(details) {
        const detailLinks = details.querySelectorAll('a');
        let hasActiveLink = false;
        
        detailLinks.forEach(function(link) {
            const linkPath = link.getAttribute('href');
            
            if (linkPath === currentPath) {
                link.classList.add('active');
                hasActiveLink = true;
            }
        });
        
        // If any link inside is active, highlight the summary and auto-open
        if (hasActiveLink) {
            const summary = details.querySelector('summary');
            summary.classList.add('active');
            details.setAttribute('open', ''); // Auto-open the details
        }
    });
});