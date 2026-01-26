document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(
        "#global-django-messages .global-message"
    );

    messages.forEach((message) => {

        // Auto dismiss after 3 seconds
        setTimeout(() => {
            removeMessage(message);
        }, 3000);

        // Close button
        const closeBtn = message.querySelector(".global-message-close");
        closeBtn.addEventListener("click", () => {
            removeMessage(message);
        });
    });

    function removeMessage(message) {
        if (!message) return;
        message.style.animation = "globalFadeOut 0.3s ease forwards";
        setTimeout(() => {
            message.remove();
        }, 300);
    }
});

