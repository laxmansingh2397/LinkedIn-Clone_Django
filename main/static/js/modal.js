document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("postModal");
    const btn = document.querySelector(".start-a-post");
    const span = document.querySelector(".close");

    if (btn) {
        btn.addEventListener("click", function () {
            modal.style.display = "block";
        });
    }

    if (span) {
        span.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
