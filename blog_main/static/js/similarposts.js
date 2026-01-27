document.addEventListener("DOMContentLoaded", function() {
    const spItems = document.querySelectorAll(".sp-blog-item");

    spItems.forEach(item => {
        item.addEventListener("mouseenter", () => {
            item.style.cursor = "pointer";
        });

        item.addEventListener("click", () => {
            const link = item.querySelector(".sp-blog-title");
            if(link) {
                window.location.href = link.href;
            }
        });
    });
});