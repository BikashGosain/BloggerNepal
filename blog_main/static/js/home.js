// ===================================
// HOME PAGE - MODERN INTERACTIONS
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initScrollAnimations();
    initContactForm();
    initReadingTime();
    initViewCounter();
    initSmoothScroll();
    initCardAnimations();
    createScrollProgress();
});

// ===================================
// SCROLL ANIMATIONS
// ===================================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Unobserve after animation to improve performance
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and sections
    const elements = document.querySelectorAll('.card, .jumbotron, h3.text-uppercase');
    elements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// ===================================
// CONTACT FORM ENHANCEMENTS
// ===================================
function initContactForm() {
    const form = document.querySelector('form[action*="contacthome"]');
    if (!form) return;

    const subjectInput = form.querySelector('input[name="subject"]');
    const messageTextarea = form.querySelector('textarea[name="message"]');
    const submitButton = form.querySelector('button[type="submit"]');

    // Add character counter to message field
    addCharacterCounter(messageTextarea);

    // Real-time validation
    if (subjectInput) {
        subjectInput.addEventListener('input', function() {
            validateInput(this, 3, 'Subject must be at least 3 characters');
        });
    }

    if (messageTextarea) {
        messageTextarea.addEventListener('input', function() {
            validateInput(this, 10, 'Message must be at least 10 characters');
        });
    }

    // Form submission handling
    form.addEventListener('submit', function(e) {
        if (submitButton && !submitButton.disabled) {
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <span style="display: inline-flex; align-items: center; gap: 8px;">
                    <span class="spinner"></span>
                    Sending...
                </span>
            `;
            
            // Add spinner styles
            const style = document.createElement('style');
            style.textContent = `
                .spinner {
                    width: 16px;
                    height: 16px;
                    border: 2px solid rgba(255,255,255,0.3);
                    border-top-color: white;
                    border-radius: 50%;
                    animation: spin 0.8s linear infinite;
                }
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
    });
}

// Validate input fields
function validateInput(input, minLength, errorMessage) {
    const value = input.value.trim();
    
    if (value.length === 0) {
        resetInputState(input);
        return;
    }
    
    if (value.length < minLength) {
        input.style.borderColor = '#dc3545';
        showTooltip(input, errorMessage, 'error');
    } else {
        input.style.borderColor = '#28a745';
        removeTooltip(input);
    }
}

// Reset input styling
function resetInputState(input) {
    input.style.borderColor = '#e9ecef';
    removeTooltip(input);
}

// Show validation tooltip
function showTooltip(element, message, type) {
    removeTooltip(element);
    
    const tooltip = document.createElement('div');
    tooltip.className = 'validation-tooltip';
    tooltip.textContent = message;
    tooltip.style.cssText = `
        position: absolute;
        bottom: -25px;
        left: 0;
        background-color: ${type === 'error' ? '#dc3545' : '#28a745'};
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        white-space: nowrap;
        z-index: 1000;
        animation: slideDown 0.3s ease;
    `;
    
    element.parentElement.style.position = 'relative';
    element.parentElement.appendChild(tooltip);
}

// Remove validation tooltip
function removeTooltip(element) {
    const tooltip = element.parentElement.querySelector('.validation-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Add character counter to textarea
function addCharacterCounter(textarea) {
    if (!textarea) return;
    
    const maxLength = 500;
    const counter = document.createElement('div');
    counter.className = 'char-counter';
    counter.style.cssText = `
        text-align: right;
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: -10px;
        margin-bottom: 15px;
    `;
    
    textarea.parentElement.insertBefore(counter, textarea.nextSibling);
    
    function updateCounter() {
        const length = textarea.value.length;
        counter.innerHTML = `<span style="color: ${length > maxLength * 0.9 ? '#dc3545' : '#6c757d'}">${length}</span> / ${maxLength}`;
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

// ===================================
// READING TIME ESTIMATOR
// ===================================
function initReadingTime() {
    const cards = document.querySelectorAll('.card-text');
    
    cards.forEach(card => {
        const text = card.textContent;
        const wordCount = text.trim().split(/\s+/).length;
        const readingTime = Math.ceil(wordCount / 200); // Average reading speed
        
        if (readingTime > 0) {
            const badge = document.createElement('span');
            badge.className = 'reading-time-badge';
            badge.innerHTML = `📖 ${readingTime} min read`;
            badge.style.cssText = `
                display: inline-block;
                background-color: #ffc107;
                color: #212529;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
                margin-left: 10px;
            `;
            
            const heading = card.closest('.card-body').querySelector('h3');
            if (heading) {
                heading.appendChild(badge);
            }
        }
    });
}

// ===================================
// VIEW COUNTER ANIMATION
// ===================================
function initViewCounter() {
    // This would typically connect to your backend
    // For now, we'll add a visual indicator for popular posts
    const cards = document.querySelectorAll('.featured-post-card, .blog-main .card');
    
    cards.forEach((card, index) => {
        // Simulate view counts (replace with actual data from backend)
        if (index < 3) {
            const badge = document.createElement('div');
            badge.className = 'popular-badge';
            badge.innerHTML = '🔥 Trending';
            badge.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
                color: white;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 700;
                box-shadow: 0 4px 12px rgba(238, 90, 111, 0.4);
                z-index: 10;
            `;
            
            card.style.position = 'relative';
            card.appendChild(badge);
        }
    });
}

// ===================================
// SMOOTH SCROLL
// ===================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===================================
// CARD HOVER ANIMATIONS
// ===================================
function initCardAnimations() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
}

// ===================================
// SCROLL PROGRESS BAR
// ===================================
function createScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 4px;
        background: linear-gradient(90deg, #ffc107 0%, #ff6b6b 100%);
        z-index: 9999;
        transition: width 0.1s ease;
        box-shadow: 0 2px 4px rgba(255, 193, 7, 0.4);
    `;
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

// ===================================
// LAZY LOADING FOR IMAGES
// ===================================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===================================
// SOCIAL SHARE BUTTONS (Optional)
// ===================================
function addSocialShare() {
    const cards = document.querySelectorAll('.blog-main .card');
    
    cards.forEach(card => {
        const shareDiv = document.createElement('div');
        shareDiv.className = 'social-share';
        shareDiv.style.cssText = `
            margin-top: 15px;
            display: flex;
            gap: 10px;
        `;
        
        const shareText = document.createElement('span');
        shareText.textContent = 'Share: ';
        shareText.style.cssText = `
            font-size: 0.85rem;
            color: #6c757d;
            margin-right: 5px;
        `;
        
        shareDiv.appendChild(shareText);
        
        // Add share buttons (Twitter, Facebook, LinkedIn)
        const platforms = [
            { name: 'Twitter', icon: '𝕏', color: '#1DA1F2' },
            { name: 'Facebook', icon: 'f', color: '#4267B2' },
            { name: 'LinkedIn', icon: 'in', color: '#0077B5' }
        ];
        
        platforms.forEach(platform => {
            const btn = document.createElement('button');
            btn.innerHTML = platform.icon;
            btn.style.cssText = `
                width: 30px;
                height: 30px;
                border-radius: 50%;
                border: none;
                background-color: ${platform.color};
                color: white;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.2)';
                this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            });
            
            shareDiv.appendChild(btn);
        });
        
        const cardBody = card.querySelector('.card-body');
        if (cardBody) {
            cardBody.appendChild(shareDiv);
        }
    });
}

// Uncomment to enable social share buttons
// addSocialShare();

// ===================================
// BACK TO TOP BUTTON
// ===================================
function createBackToTop() {
    const btn = document.createElement('button');
    btn.innerHTML = '↑';
    btn.className = 'back-to-top';
    btn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #ffc107 0%, #ff6b6b 100%);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 16px rgba(255, 193, 7, 0.4);
    `;
    
    document.body.appendChild(btn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            btn.style.opacity = '1';
            btn.style.visibility = 'visible';
        } else {
            btn.style.opacity = '0';
            btn.style.visibility = 'hidden';
        }
    });
    
    btn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    btn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) rotate(360deg)';
    });
    
    btn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
    });
}

createBackToTop();