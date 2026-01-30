// Minimal JavaScript for Followers List Page

// Loading state for action buttons
document.addEventListener('DOMContentLoaded', function() {
    const actionButtons = document.querySelectorAll('.action-btn');
    
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('loading');
            this.style.pointerEvents = 'none';
        });
    });
    
    console.log('Followers page loaded');
});

document.addEventListener("DOMContentLoaded", function () {
    const clearBtn = document.getElementById("clearSearchBtn");
    const searchInput = document.getElementById("follower-search");

    if (clearBtn) {
        clearBtn.addEventListener("click", function () {
            searchInput.value = "";
        });
    }
});



