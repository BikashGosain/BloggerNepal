// // ===================================
// // RECENT POSTS - PAGINATION & INTERACTIONS
// // ===================================

// document.addEventListener('DOMContentLoaded', function() {
//     initRecentPostsPagination();
// });

// function initRecentPostsPagination() {
//     const itemsPerPageSelect = document.getElementById('recent-items-per-page');
//     const paginationContainer = document.getElementById('recent-pagination-container');
//     const postsGrid = document.querySelector('.recent-posts-grid');
    
//     if (!postsGrid || !paginationContainer) return;
    
//     const allPosts = Array.from(document.querySelectorAll('.recent-post-item'));
    
//     if (allPosts.length === 0) return;
    
//     let currentPage = 1;
//     let itemsPerPage = parseInt(itemsPerPageSelect.value);
    
//     // Items per page change handler
//     itemsPerPageSelect.addEventListener('change', function() {
//         itemsPerPage = parseInt(this.value);
//         currentPage = 1;
//         renderPagination();
//     });
    
//     function showPage(page) {
//     allPosts.forEach(post => {
//         post.style.display = 'none';
//     });

//     const startIndex = (page - 1) * itemsPerPage;
//     const endIndex = startIndex + itemsPerPage;

//     const postsToShow = allPosts.slice(startIndex, endIndex);
//     postsToShow.forEach((post, index) => {
//         post.style.display = 'block';
//         post.style.animation = 'none';
//         setTimeout(() => {
//             post.style.animation = `slideInRight 0.6s ease-out forwards ${index * 0.1}s`;
//         }, 10);
//     });

//     // 🚫 DO NOT scroll on initial load
//     if (!isInitialLoad) {
//         const section = document.querySelector('.recent-posts-section');
//         if (section) {
//             section.scrollIntoView({ behavior: 'smooth', block: 'start' });
//         }
//     }
// }

    
//     function renderPagination() {
//         const totalPages = Math.ceil(allPosts.length / itemsPerPage);
        
//         if (totalPages <= 1) {
//             paginationContainer.innerHTML = '';
//             showPage(1);
//             return;
//         }
        
//         let paginationHTML = '';
        
//         // First page button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="recentGoToPage(1)" 
//                     ${currentPage === 1 ? 'disabled' : ''}
//                     title="First Page">
//                 <i class="fas fa-angle-double-left"></i> First
//             </button>
//         `;
        
//         // Previous button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="recentGoToPage(${currentPage - 1})" 
//                     ${currentPage === 1 ? 'disabled' : ''}
//                     title="Previous Page">
//                 <i class="fas fa-chevron-left"></i> Previous
//             </button>
//         `;
        
//         // Page numbers
//         const maxVisiblePages = 5;
//         let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
//         let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
        
//         if (endPage - startPage < maxVisiblePages - 1) {
//             startPage = Math.max(1, endPage - maxVisiblePages + 1);
//         }
        
//         // First page
//         if (startPage > 1) {
//             paginationHTML += `
//                 <button class="pagination-btn" onclick="recentGoToPage(1)">1</button>
//             `;
//             if (startPage > 2) {
//                 paginationHTML += `<span class="pagination-info">...</span>`;
//             }
//         }
        
//         // Page numbers
//         for (let i = startPage; i <= endPage; i++) {
//             paginationHTML += `
//                 <button class="pagination-btn ${i === currentPage ? 'active' : ''}" 
//                         onclick="recentGoToPage(${i})">
//                     ${i}
//                 </button>
//             `;
//         }
        
//         // Last page
//         if (endPage < totalPages) {
//             if (endPage < totalPages - 1) {
//                 paginationHTML += `<span class="pagination-info">...</span>`;
//             }
//             paginationHTML += `
//                 <button class="pagination-btn" onclick="recentGoToPage(${totalPages})">
//                     ${totalPages}
//                 </button>
//             `;
//         }
        
//         // Next button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="recentGoToPage(${currentPage + 1})" 
//                     ${currentPage === totalPages ? 'disabled' : ''}
//                     title="Next Page">
//                 Next <i class="fas fa-chevron-right"></i>
//             </button>
//         `;
        
//         // Last page button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="recentGoToPage(${totalPages})" 
//                     ${currentPage === totalPages ? 'disabled' : ''}
//                     title="Last Page">
//                 Last <i class="fas fa-angle-double-right"></i>
//             </button>
//         `;
        
//         // Page info
//         paginationHTML += `
//             <span class="pagination-info">
//                 Page ${currentPage} of ${totalPages}
//             </span>
//         `;
        
//         paginationContainer.innerHTML = paginationHTML;
//         showPage(currentPage);
//     }
    
//     // Global function for pagination buttons
//     window.recentGoToPage = function(page) {
//         const totalPages = Math.ceil(allPosts.length / itemsPerPage);
//         if (page < 1 || page > totalPages) return;
//         currentPage = page;
//         renderPagination();
//     };
    
//     // Initial render
//     renderPagination();
// }

// // ===================================
// // RECENT POSTS - HOVER EFFECTS
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const recentCards = document.querySelectorAll('.recent-post-card');
    
//     recentCards.forEach(card => {
//         // Add smooth transition on hover
//         card.addEventListener('mouseenter', function() {
//             this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
//         });
        
//         card.addEventListener('mouseleave', function() {
//             this.style.transition = 'all 0.3s ease';
//         });
//     });
// });

// // ===================================
// // READ MORE LINK ANIMATION
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const readMoreLinks = document.querySelectorAll('.read-more-link');
    
//     readMoreLinks.forEach(link => {
//         link.addEventListener('mouseenter', function() {
//             const icon = this.querySelector('i');
//             if (icon) {
//                 icon.style.transform = 'translateX(5px)';
//             }
//         });
        
//         link.addEventListener('mouseleave', function() {
//             const icon = this.querySelector('i');
//             if (icon) {
//                 icon.style.transform = 'translateX(0)';
//             }
//         });
//     });
// });

// // ===================================
// // STATS COUNTER ANIMATION
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const statBadges = document.querySelectorAll('.recent-post-card .stat-badge');
    
//     // Intersection Observer for counter animation
//     const observerOptions = {
//         threshold: 0.5,
//         rootMargin: '0px'
//     };
    
//     const observer = new IntersectionObserver(function(entries) {
//         entries.forEach(entry => {
//             if (entry.isIntersecting) {
//                 const badge = entry.target;
//                 const icon = badge.querySelector('i');
//                 const textNode = Array.from(badge.childNodes).find(node => node.nodeType === 3);
                
//                 if (textNode) {
//                     const finalValue = parseInt(textNode.textContent.trim());
//                     if (!isNaN(finalValue) && finalValue > 0) {
//                         animateCounter(badge, textNode, finalValue);
//                     }
//                 }
                
//                 observer.unobserve(badge);
//             }
//         });
//     }, observerOptions);
    
//     statBadges.forEach(badge => {
//         observer.observe(badge);
//     });
    
//     function animateCounter(badge, textNode, finalValue) {
//         let current = 0;
//         const increment = Math.ceil(finalValue / 30);
//         const duration = 1000;
//         const stepTime = duration / (finalValue / increment);
        
//         const timer = setInterval(() => {
//             current += increment;
//             if (current >= finalValue) {
//                 current = finalValue;
//                 clearInterval(timer);
//             }
//             textNode.textContent = ` ${current} `;
//         }, stepTime);
//     }
// });

// // ===================================
// // CATEGORY BADGE ANIMATION
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const categoryBadges = document.querySelectorAll('.recent-post-card .recent-category-badge');
    
//     categoryBadges.forEach(badge => {
//         badge.style.cursor = 'pointer';
        
//         badge.addEventListener('mouseenter', function() {
//             this.style.transform = 'scale(1.1)';
//             this.style.transition = 'transform 0.3s ease';
//         });
        
//         badge.addEventListener('mouseleave', function() {
//             this.style.transform = 'scale(1)';
//         });
        
//         badge.addEventListener('click', function(e) {
//             e.preventDefault();
//             e.stopPropagation();
            
//             const category = this.textContent.trim();
//             console.log('Category clicked:', category);
            
//             // You can implement category filtering here
//             // Or redirect to category page
//             // window.location.href = `/category/${category.toLowerCase()}`;
//         });
//     });
// });

// // ===================================
// // IMAGE LAZY LOADING (Optional)
// // ===================================
// if ('IntersectionObserver' in window) {
//     document.addEventListener('DOMContentLoaded', function() {
//         const imageObserver = new IntersectionObserver((entries, observer) => {
//             entries.forEach(entry => {
//                 if (entry.isIntersecting) {
//                     const img = entry.target;
//                     if (img.dataset.src) {
//                         img.src = img.dataset.src;
//                         img.classList.add('loaded');
//                         observer.unobserve(img);
//                     }
//                 }
//             });
//         });
        
//         document.querySelectorAll('.recent-post-image[data-src]').forEach(img => {
//             imageObserver.observe(img);
//         });
//     });
// }

// // ===================================
// // CARD CLICK TO POST (Optional)
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const recentCards = document.querySelectorAll('.recent-post-card');
    
//     recentCards.forEach(card => {
//         // Make entire card clickable (optional)
//         card.style.cursor = 'pointer';
        
//         card.addEventListener('click', function(e) {
//             // Don't trigger if clicking on links or buttons
//             if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
//                 return;
//             }
            
//             const link = this.querySelector('.recent-post-title a');
//             if (link) {
//                 window.location.href = link.href;
//             }
//         });
//     });
// });