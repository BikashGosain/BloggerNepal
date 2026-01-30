// Profile Pagination Script
document.addEventListener('DOMContentLoaded', function() {
    const blogGrid = document.querySelector('.blog-grid');
    const paginationContainer = document.getElementById('pagination-container');
    
    if (!blogGrid || !paginationContainer) return;
    
    const blogItems = Array.from(document.querySelectorAll('.blog-item'));
    let currentPage = 1;
    let itemsPerPage = parseInt(document.getElementById('items-per-page')?.value) || 6;
    
    // Initialize pagination
    function initPagination() {
        if (blogItems.length === 0) {
            paginationContainer.style.display = 'none';
            return;
        }
        
        renderPagination();
        showPage(currentPage);
    }
    
    // Show specific page
    function showPage(page) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        
        // Add loading effect
        blogGrid.classList.add('loading');
        
        // Hide all items
        blogItems.forEach((item, index) => {
            item.style.display = 'none';
            item.style.animation = 'none';
        });
        
        // Small delay for loading effect
        setTimeout(() => {
            // Show items for current page
            blogItems.slice(startIndex, endIndex).forEach((item, index) => {
                item.style.display = 'block';
                // Reset animation
                void item.offsetWidth; // Trigger reflow
                item.style.animation = `fadeIn 0.5s ease-in-out ${index * 0.1}s forwards`;
            });
            
            blogGrid.classList.remove('loading');
            
            // Scroll to posts section smoothly
            const postsSection = document.querySelector('.posts-section');
            if (postsSection) {
                const offsetTop = postsSection.offsetTop - 100;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }, 200);
        
        currentPage = page;
        updatePaginationButtons();
        updatePageInfo();
    }
    
    // Render pagination buttons
    function renderPagination() {
        const totalPages = Math.ceil(blogItems.length / itemsPerPage);
        
        if (totalPages <= 1) {
            paginationContainer.style.display = 'none';
            return;
        }
        
        paginationContainer.style.display = 'flex';
        
        let paginationHTML = '<div class="pagination-wrapper">';
        
        // Previous button
        paginationHTML += `
            <button class="pagination-btn prev-btn" id="prev-page" ${currentPage === 1 ? 'disabled' : ''}>
                <i class="fas fa-chevron-left"></i> Prev
            </button>
        `;
        
        // Page numbers with smart ellipsis
        const pageNumbers = generatePageNumbers(totalPages);
        
        pageNumbers.forEach(num => {
            if (num === '...') {
                paginationHTML += '<span class="pagination-ellipsis">...</span>';
            } else {
                paginationHTML += `
                    <button class="pagination-btn page-num ${num === currentPage ? 'active' : ''}" 
                            data-page="${num}">
                        ${num}
                    </button>
                `;
            }
        });
        
        // Next button
        paginationHTML += `
            <button class="pagination-btn next-btn" id="next-page" ${currentPage === totalPages ? 'disabled' : ''}>
                Next <i class="fas fa-chevron-right"></i>
            </button>
        `;
        
        paginationHTML += '</div>';
        
        // Page info
        const startItem = (currentPage - 1) * itemsPerPage + 1;
        const endItem = Math.min(currentPage * itemsPerPage, blogItems.length);
        
        paginationHTML += `
            <div class="page-info">
                <i class="fas fa-info-circle"></i>
                <span class="page-info-text">
                    Showing ${startItem}-${endItem} of ${blogItems.length} posts
                </span>
            </div>
        `;
        
        paginationContainer.innerHTML = paginationHTML;
        
        // Add event listeners
        attachPaginationEvents();
    }
    
    // Generate smart page numbers with ellipsis
    function generatePageNumbers(totalPages) {
        const delta = 2; // Number of pages to show on each side of current page
        const range = [];
        const rangeWithDots = [];
        let l;
        
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - delta && i <= currentPage + delta)) {
                range.push(i);
            }
        }
        
        range.forEach(i => {
            if (l) {
                if (i - l === 2) {
                    rangeWithDots.push(l + 1);
                } else if (i - l !== 1) {
                    rangeWithDots.push('...');
                }
            }
            rangeWithDots.push(i);
            l = i;
        });
        
        return rangeWithDots;
    }
    
    // Attach event listeners to pagination buttons
    function attachPaginationEvents() {
        // Previous button
        const prevBtn = document.getElementById('prev-page');
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentPage > 1) {
                    showPage(currentPage - 1);
                }
            });
        }
        
        // Next button
        const nextBtn = document.getElementById('next-page');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                const totalPages = Math.ceil(blogItems.length / itemsPerPage);
                if (currentPage < totalPages) {
                    showPage(currentPage + 1);
                }
            });
        }
        
        // Page number buttons
        const pageButtons = document.querySelectorAll('.pagination-btn.page-num');
        pageButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const page = parseInt(btn.dataset.page);
                showPage(page);
            });
        });
    }
    
    // Update pagination button states
    function updatePaginationButtons() {
        const totalPages = Math.ceil(blogItems.length / itemsPerPage);
        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        
        if (prevBtn) {
            prevBtn.disabled = currentPage === 1;
        }
        
        if (nextBtn) {
            nextBtn.disabled = currentPage === totalPages;
        }
        
        // Update active page button
        document.querySelectorAll('.pagination-btn.page-num').forEach(btn => {
            const page = parseInt(btn.dataset.page);
            btn.classList.toggle('active', page === currentPage);
        });
    }
    
    // Update page info
    function updatePageInfo() {
        const pageInfo = document.querySelector('.page-info-text');
        if (pageInfo) {
            const startItem = (currentPage - 1) * itemsPerPage + 1;
            const endItem = Math.min(currentPage * itemsPerPage, blogItems.length);
            pageInfo.textContent = `Showing ${startItem}-${endItem} of ${blogItems.length} posts`;
        }
    }
    
    // Items per page change handler
    const itemsPerPageSelect = document.getElementById('items-per-page');
    if (itemsPerPageSelect) {
        itemsPerPageSelect.addEventListener('change', function() {
            itemsPerPage = parseInt(this.value);
            currentPage = 1; // Reset to first page
            renderPagination();
            showPage(1);
        });
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        const totalPages = Math.ceil(blogItems.length / itemsPerPage);
        
        // Don't interfere if user is typing in an input
        if (document.activeElement.tagName === 'INPUT' || 
            document.activeElement.tagName === 'TEXTAREA') {
            return;
        }
        
        // Left arrow - previous page
        if (e.key === 'ArrowLeft' && currentPage > 1) {
            e.preventDefault();
            showPage(currentPage - 1);
        }
        
        // Right arrow - next page
        if (e.key === 'ArrowRight' && currentPage < totalPages) {
            e.preventDefault();
            showPage(currentPage + 1);
        }
    });
    
    // Initialize on load
    initPagination();
});