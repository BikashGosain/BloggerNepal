        document.addEventListener("DOMContentLoaded", function () {
            const toasts = document.querySelectorAll(".toast");

            toasts.forEach((toast) => {
                setTimeout(() => {
                    toast.classList.add("hide");
                    setTimeout(() => toast.remove(), 400);
                }, 5000);
            });

            // Init TinyMCE only if textarea exists
            if (document.getElementById("id_blog_body")) {
                tinymce.init({
                    selector: '#id_blog_body',
                    height: 400,
                    menubar: true,
                    plugins: 'lists link image code preview',
                    toolbar:
                        'undo redo | bold italic | alignleft aligncenter alignright | bullist numlist | code preview',
                });
            }

            // Mobile menu toggle
            const menuToggle = document.getElementById('mobile-menu-toggle');
            const mobileMenu = document.getElementById('mobile-menu');

            if (menuToggle && mobileMenu) {
                menuToggle.addEventListener('click', function () {
                    mobileMenu.classList.toggle('active');
                    const icon = this.querySelector('i');
                    if (mobileMenu.classList.contains('active')) {
                        icon.classList.remove('fa-bars');
                        icon.classList.add('fa-times');
                    } else {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                });
            }

            // Mobile category toggle
            const categoryToggle = document.getElementById('mobile-category-toggle');
            const categoryList = document.getElementById('mobile-category-list');

            if (categoryToggle && categoryList) {
                categoryToggle.addEventListener('click', function () {
                    categoryList.classList.toggle('active');
                    const icon = this.querySelector('i');
                    if (categoryList.classList.contains('active')) {
                        icon.classList.remove('fa-caret-right');
                        icon.classList.add('fa-caret-down');
                    } else {
                        icon.classList.remove('fa-caret-down');
                        icon.classList.add('fa-caret-right');
                    }
                });
            }

            // Desktop category dropdown for mobile
            const categoryBtn = document.querySelector('.category-btn');
            const categoryDropdown = document.querySelector('.category-dropdown-content');

            if (categoryBtn && categoryDropdown && window.innerWidth <= 768) {
                categoryBtn.addEventListener('click', function (e) {
                    e.preventDefault();
                    categoryDropdown.style.display =
                        categoryDropdown.style.display === 'block' ? 'none' : 'block';
                });

                // Close dropdown when clicking outside
                document.addEventListener('click', function (e) {
                    if (!e.target.closest('.category-dropdown')) {
                        categoryDropdown.style.display = 'none';
                    }
                });
            }
        });

        function closeToast(element) {
            const toast = element.parentElement;
            toast.classList.add("hide");
            setTimeout(() => toast.remove(), 400);
        }

        function toggleReplyForm(commentId) {
            const form = document.getElementById(`reply-form-${commentId}`);
            if (form) {
                form.classList.toggle('d-none');
            }
        }

        function confirmLogout() {
            return confirm("Are you sure you want to logout?");
        }
        document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('mobile-social_links-toggle');
    const list = document.getElementById('mobile-social_links-list');

    toggleBtn.addEventListener('click', function() {
        if(list.style.display === 'none' || list.style.display === '') {
            list.style.display = 'block';
            toggleBtn.querySelector('i').classList.remove('fa-caret-right');
            toggleBtn.querySelector('i').classList.add('fa-caret-down');
        } else {
            list.style.display = 'none';
            toggleBtn.querySelector('i').classList.remove('fa-caret-down');
            toggleBtn.querySelector('i').classList.add('fa-caret-right');
        }
    });
});
