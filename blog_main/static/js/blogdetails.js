/**
 * ============================================
 * Blog Details - Complete JavaScript
 * Handles comments, replies, edit, delete, and modals
 * ============================================
 */

(function() {
    'use strict';

    // ============================================
    // Utility Functions
    // ============================================

    /**
     * Get CSRF token from cookies
     */
    function getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Show toast notification
     */
    function showToast(message, type = 'info') {
        const container = document.getElementById('bd-toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `bd-toast bd-toast-${type}`;
        
        const icons = {
            success: '<i class="fas fa-check-circle"></i>',
            error: '<i class="fas fa-exclamation-circle"></i>',
            warning: '<i class="fas fa-exclamation-triangle"></i>',
            info: '<i class="fas fa-info-circle"></i>'
        };

        toast.innerHTML = `
            <div class="bd-toast-icon">${icons[type] || icons.info}</div>
            <div class="bd-toast-content">
                <div class="bd-toast-message">${message}</div>
            </div>
            <button class="bd-toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;

        container.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.classList.add('bd-hiding');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }


    

    /**
     * Update comment count
     */
    function updateCommentCount(change) {
        const countElement = document.getElementById('bd-comment-count');
        if (countElement) {
            const currentCount = parseInt(countElement.textContent) || 0;
            const newCount = Math.max(0, currentCount + change);
            countElement.textContent = newCount;
        }
    }

    /**
     * Smooth scroll to element
     */
    function smoothScrollTo(element) {
        if (element) {
            element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }
    }

    // ============================================
    // Comment Functions
    // ============================================

    /**
     * Toggle reply form
     */
    window.bdToggleReplyForm = function(commentId) {
        const replyForm = document.getElementById(`bd-reply-form-${commentId}`);
        if (!replyForm) return;

        // Close all other reply forms
        document.querySelectorAll('.bd-reply-form').forEach(form => {
            if (form.id !== `bd-reply-form-${commentId}`) {
                form.classList.add('bd-hidden');
            }
        });

        // Toggle current form
        replyForm.classList.toggle('bd-hidden');

        if (!replyForm.classList.contains('bd-hidden')) {
            const textarea = replyForm.querySelector('textarea[name="comment"]');
            if (textarea) {
                setTimeout(() => textarea.focus(), 100);
            }
        }
    };
    window.bdSubmitMainComment = function(event) {
    event.preventDefault();

    const form = event.target;
    const textarea = form.querySelector('textarea[name="comment"]');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (!textarea.value.trim()) {
        showToast('Please enter a comment', 'warning');
        textarea.focus();
        return false;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Posting...';

    const formData = new FormData(form);

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.text();
    })
    .then(() => {
        showToast('Comment posted successfully!', 'success');

        textarea.value = '';

        // ✅ safest approach for nested comments
        location.reload();
    })
    .catch(() => {
        showToast('Failed to post comment', 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Post Comment';
    });

    return false;
};


    /**
     * Submit reply (called on form submit)
     */
    window.bdSubmitReply = function(event, commentId) {
    event.preventDefault();

    const form = event.target;
    const textarea = form.querySelector('textarea[name="comment"]');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (!textarea.value.trim()) {
        showToast('Please enter a reply', 'warning');
        return false;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Posting...';

    const formData = new FormData(form);

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.text();
    })
    .then(() => {
        showToast('Reply posted successfully!', 'success');
        textarea.value = '';
        bdToggleReplyForm(commentId);

        // 🔁 Reload only comments section (simple & safe)
        location.reload();
    })
    .catch(() => {
        showToast('Failed to post reply', 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Reply';
    });

    return false;
};


    /**
     * Toggle edit form
     */
    window.bdToggleEditForm = function(commentId) {
        const editForm = document.getElementById(`bd-edit-form-${commentId}`);
        const commentText = document.getElementById(`bd-comment-text-${commentId}`);
        
        if (!editForm || !commentText) return;

        // Close all other edit forms
        document.querySelectorAll('.bd-edit-form').forEach(form => {
            if (form.id !== `bd-edit-form-${commentId}`) {
                form.classList.add('bd-hidden');
                const otherId = form.id.replace('bd-edit-form-', '');
                const otherText = document.getElementById(`bd-comment-text-${otherId}`);
                if (otherText) otherText.classList.remove('bd-hidden');
            }
        });

        // Toggle current form
        if (editForm.classList.contains('bd-hidden')) {
            editForm.classList.remove('bd-hidden');
            commentText.classList.add('bd-hidden');
            
            const textarea = editForm.querySelector('textarea');
            if (textarea) {
                setTimeout(() => {
                    textarea.focus();
                    textarea.setSelectionRange(textarea.value.length, textarea.value.length);
                }, 100);
            }
        } else {
            editForm.classList.add('bd-hidden');
            commentText.classList.remove('bd-hidden');
        }
    };

    /**
     * Submit edit
     */
    window.bdSubmitEdit = function(commentId, url) {
    const textarea = document.getElementById(`bd-edit-text-${commentId}`);
    const commentText = document.getElementById(`bd-comment-text-${commentId}`);

    if (!textarea || !commentText) return;

    const newText = textarea.value.trim();

    if (!newText) {
        showToast('Comment cannot be empty', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('comment', newText);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            commentText.textContent = data.comment;
            document.getElementById(`bd-edit-form-${commentId}`).classList.add('bd-hidden');
            commentText.classList.remove('bd-hidden');
            showToast('Comment updated successfully!', 'success');
        } else {
            showToast(data.error || 'Edit failed', 'error');
        }
    })
    .catch(() => showToast('Server error', 'error'));
};


    /**
     * Delete comment
     */
    window.bdDeleteComment = function(url) {
    if (!confirm('Delete this comment?')) return;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const id = url.split('/').filter(Boolean).pop();
            document.getElementById(`bd-comment-${id}`)?.remove();
            updateCommentCount(-1);
            showToast('Comment deleted', 'success');
        } else {
            showToast(data.error || 'Delete failed', 'error');
        }
    })
    .catch(() => showToast('Server error', 'error'));
};


    // ============================================
    // Report Modal Functions
    // ============================================

    /**
     * Open report modal
     */
    window.bdOpenReportModal = function() {
        const modal = document.getElementById('bd-report-modal');
        if (modal) {
            modal.classList.add('bd-show');
            document.body.style.overflow = 'hidden';
            
            const textarea = modal.querySelector('textarea[name="reason"]');
            if (textarea) {
                setTimeout(() => textarea.focus(), 100);
            }
        }
    };

    /**
     * Close report modal
     */
    window.bdCloseReportModal = function() {
        const modal = document.getElementById('bd-report-modal');
        if (modal) {
            modal.classList.remove('bd-show');
            document.body.style.overflow = '';
            
            const textarea = modal.querySelector('textarea[name="reason"]');
            if (textarea) {
                textarea.value = '';
            }
        }
    };

    // Close modal on Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            bdCloseReportModal();
            
            // Also close any open reply/edit forms
            document.querySelectorAll('.bd-reply-form, .bd-edit-form').forEach(form => {
                form.classList.add('bd-hidden');
            });
            
            // Show hidden comment texts
            document.querySelectorAll('.bd-comment-text.bd-hidden').forEach(text => {
                text.classList.remove('bd-hidden');
            });
        }
    });

    // ============================================
    // Auto-resize Textareas
    // ============================================

    function setupTextareaAutoResize() {
        const textareas = document.querySelectorAll('.bd-textarea');
        
        textareas.forEach(textarea => {
            // Auto-resize on input
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        });
    }

    // ============================================
    // Like/Dislike Animation (Optional)
    // ============================================

    function setupLikeDislikeAnimation() {
        const likeBtn = document.querySelector('.bd-like-btn');
        const dislikeBtn = document.querySelector('.bd-dislike-btn');

        if (likeBtn) {
            likeBtn.addEventListener('click', function(e) {
                // Optional: Add animation or AJAX handling here
                // For now, it will follow the link normally
            });
        }

        if (dislikeBtn) {
            dislikeBtn.addEventListener('click', function(e) {
                // Optional: Add animation or AJAX handling here
                // For now, it will follow the link normally
            });
        }
    }

    // ============================================
    // Form Validation
    // ============================================

    function setupFormValidation() {
        

        // Reply forms (delegated event listener)
        document.addEventListener('submit', function(e) {
            if (e.target.classList.contains('bd-reply-form')) {
                const textarea = e.target.querySelector('textarea[name="comment"]');
                if (!textarea.value.trim()) {
                    e.preventDefault();
                    showToast('Please enter a reply', 'warning');
                    textarea.focus();
                    return false;
                }
            }
        });
    }

    // ============================================
    // Smooth Scroll to New Comment
    // ============================================

    function scrollToNewComment() {
        // Check if URL has a hash for comment
        const hash = window.location.hash;
        if (hash && hash.startsWith('#bd-comment-')) {
            const commentElement = document.querySelector(hash);
            if (commentElement) {
                setTimeout(() => {
                    smoothScrollTo(commentElement);
                    // Highlight the comment
                    commentElement.style.animation = 'bdHighlight 2s ease';
                }, 500);
            }
        }
    }

    // ============================================
    // Reading Progress (Optional Enhancement)
    // ============================================

    function setupReadingProgress() {
        // Create progress bar
        const progressBar = document.createElement('div');
        progressBar.className = 'bd-reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--bd-primary), var(--bd-primary-light));
            z-index: 9998;
            transition: width 0.1s ease;
            box-shadow: 0 2px 5px rgba(99, 102, 241, 0.3);
        `;
        document.body.appendChild(progressBar);

        // Update on scroll
        function updateProgress() {
            const article = document.querySelector('.bd-article');
            if (!article) return;

            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const docHeight = article.offsetHeight;
            const winHeight = window.innerHeight;
            const scrollPercent = scrollTop / (docHeight - winHeight);
            const scrollPercentRounded = Math.round(scrollPercent * 100);
            
            progressBar.style.width = Math.min(scrollPercentRounded, 100) + '%';
        }

        window.addEventListener('scroll', updateProgress);
        updateProgress();
    }

    // ============================================
    // Back to Top Button
    // ============================================

    function setupBackToTop() {
        const button = document.createElement('button');
        button.className = 'bd-back-to-top';
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.setAttribute('aria-label', 'Back to top');
        button.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: var(--bd-primary);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 1.25rem;
            cursor: pointer;
            box-shadow: var(--bd-shadow-lg);
            opacity: 0;
            visibility: hidden;
            transform: translateY(20px);
            transition: all 0.3s ease;
            z-index: 999;
        `;
        document.body.appendChild(button);

        // Show/hide on scroll
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                button.style.opacity = '1';
                button.style.visibility = 'visible';
                button.style.transform = 'translateY(0)';
            } else {
                button.style.opacity = '0';
                button.style.visibility = 'hidden';
                button.style.transform = 'translateY(20px)';
            }
        });

        // Scroll to top on click
        button.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ============================================
    // Highlight Animation
    // ============================================

    function injectHighlightAnimation() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes bdHighlight {
                0%, 100% { background-color: transparent; }
                50% { background-color: rgba(99, 102, 241, 0.1); }
            }
        `;
        document.head.appendChild(style);
    }

    // ============================================
    // Initialize
    // ============================================

    function init() {
        console.log('Blog Details JS Initialized');
        
        // Setup all features
        setupTextareaAutoResize();
        setupLikeDislikeAnimation();
        setupFormValidation();
        scrollToNewComment();
        setupReadingProgress();
        setupBackToTop();
        injectHighlightAnimation();

        // Show success message if comment was just posted
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('comment') === 'posted') {
            setTimeout(() => {
                showToast('Comment posted successfully!', 'success');
            }, 500);
        }
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();