// // ===================================
// // FEATURED POSTS - PAGINATION & INTERACTIONS
// // ===================================

// document.addEventListener('DOMContentLoaded', function() {
//     initFeaturedPostsPagination();
// });

// function initFeaturedPostsPagination() {
//     const itemsPerPageSelect = document.getElementById('featured-items-per-page');
//     const paginationContainer = document.getElementById('featured-pagination-container');
//     const postsGrid = document.querySelector('.featured-posts-grid');
    
//     if (!postsGrid || !paginationContainer) return;
    
//     const allPosts = Array.from(document.querySelectorAll('.featured-post-item'));
    
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
//         // Hide all posts
//         allPosts.forEach(post => {
//             post.style.display = 'none';
//         });
        
//         // Calculate start and end indices
//         const startIndex = (page - 1) * itemsPerPage;
//         const endIndex = startIndex + itemsPerPage;
        
//         // Show posts for current page
//         const postsToShow = allPosts.slice(startIndex, endIndex);
//         postsToShow.forEach((post, index) => {
//             post.style.display = 'block';
//             // Reset animation
//             post.style.animation = 'none';
//             setTimeout(() => {
//                 post.style.animation = `fadeInUp 0.6s ease-out forwards ${index * 0.1}s`;
//             }, 10);
//         });
        
//         // Scroll to top of section
//         const section = document.querySelector('.featured-posts-section');
//         if (section) {
//             section.scrollIntoView({ behavior: 'smooth', block: 'start' });
//         }
//     }
    
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
//                     onclick="featuredGoToPage(1)" 
//                     ${currentPage === 1 ? 'disabled' : ''}
//                     title="First Page">
//                 <i class="fas fa-angle-double-left"></i> First
//             </button>
//         `;
        
//         // Previous button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="featuredGoToPage(${currentPage - 1})" 
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
//                 <button class="pagination-btn" onclick="featuredGoToPage(1)">1</button>
//             `;
//             if (startPage > 2) {
//                 paginationHTML += `<span class="pagination-info">...</span>`;
//             }
//         }
        
//         // Page numbers
//         for (let i = startPage; i <= endPage; i++) {
//             paginationHTML += `
//                 <button class="pagination-btn ${i === currentPage ? 'active' : ''}" 
//                         onclick="featuredGoToPage(${i})">
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
//                 <button class="pagination-btn" onclick="featuredGoToPage(${totalPages})">
//                     ${totalPages}
//                 </button>
//             `;
//         }
        
//         // Next button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="featuredGoToPage(${currentPage + 1})" 
//                     ${currentPage === totalPages ? 'disabled' : ''}
//                     title="Next Page">
//                 Next <i class="fas fa-chevron-right"></i>
//             </button>
//         `;
        
//         // Last page button
//         paginationHTML += `
//             <button class="pagination-btn" 
//                     onclick="featuredGoToPage(${totalPages})" 
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
//     window.featuredGoToPage = function(page) {
//         const totalPages = Math.ceil(allPosts.length / itemsPerPage);
//         if (page < 1 || page > totalPages) return;
//         currentPage = page;
//         renderPagination();
//     };
    
//     // Initial render
//     renderPagination();
// }

// // ===================================
// // FEATURED POSTS - HOVER EFFECTS
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const featuredCards = document.querySelectorAll('.featured-post-card');
    
//     featuredCards.forEach(card => {
//         // Add smooth transition on hover
//         card.addEventListener('mouseenter', function() {
//             this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
//         });
        
//         // Track mouse movement for subtle tilt effect (optional)
//         card.addEventListener('mousemove', function(e) {
//             const rect = this.getBoundingClientRect();
//             const x = e.clientX - rect.left;
//             const y = e.clientY - rect.top;
            
//             const centerX = rect.width / 2;
//             const centerY = rect.height / 2;
            
//             const rotateX = (y - centerY) / 20;
//             const rotateY = (centerX - x) / 20;
            
//             // Subtle 3D effect (comment out if not desired)
//             // this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
//         });
        
//         card.addEventListener('mouseleave', function() {
//             this.style.transform = '';
//         });
//     });
// });

// // ===================================
// // STATS BADGE ANIMATION
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const statBadges = document.querySelectorAll('.featured-post-card .stat-badge');
    
//     statBadges.forEach(badge => {
//         badge.addEventListener('mouseenter', function() {
//             // Add pulse animation
//             this.style.animation = 'pulse 0.5s ease';
//         });
        
//         badge.addEventListener('animationend', function() {
//             this.style.animation = '';
//         });
//     });
    
//     // Add pulse animation to CSS dynamically
//     if (!document.getElementById('featured-pulse-animation')) {
//         const style = document.createElement('style');
//         style.id = 'featured-pulse-animation';
//         style.textContent = `
//             @keyframes pulse {
//                 0%, 100% { transform: scale(1); }
//                 50% { transform: scale(1.15); }
//             }
//         `;
//         document.head.appendChild(style);
//     }
// });

// // ===================================
// // CATEGORY BADGE CLICK (Optional Analytics)
// // ===================================
// document.addEventListener('DOMContentLoaded', function() {
//     const categoryBadges = document.querySelectorAll('.featured-post-card .post-category-badge');
    
//     categoryBadges.forEach(badge => {
//         badge.style.cursor = 'pointer';
        
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