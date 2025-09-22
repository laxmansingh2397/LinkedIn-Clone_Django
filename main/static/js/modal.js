document.addEventListener("DOMContentLoaded", function () {
    // Main start-a-post modal
    const postModal = document.getElementById("postModal");
    const startBtn = document.querySelector(".start-a-post");

    // Photo/Video/Article modals
    const photoModal = document.getElementById("photoModal");
    const videoModal = document.getElementById("videoModal");
    const articleModal = document.getElementById("articleModal");

    // Close buttons (for all modals)
    const closeBtns = document.querySelectorAll(".close");

    // Open start-a-post modal
    if (startBtn) {
        startBtn.addEventListener("click", function () {
            postModal.style.display = "block";
        });
    }

    // Open Photo modal
    const photoBtn = document.querySelector("button:has(i.fa-image)");
    if (photoBtn && photoModal) {
        photoBtn.addEventListener("click", () => {
            photoModal.style.display = "block";
        });
    }

    // Open Video modal
    const videoBtn = document.querySelector("button:has(i.fa-video)");
    if (videoBtn && videoModal) {
        videoBtn.addEventListener("click", () => {
            videoModal.style.display = "block";
        });
    }

    // Open Article modal
    const articleBtn = document.querySelector("button:has(i.fa-newspaper)");
    if (articleBtn && articleModal) {
        articleBtn.addEventListener("click", () => {
            articleModal.style.display = "block";
        });
    }

    // Close modals on "x"
    closeBtns.forEach(span => {
        span.addEventListener("click", function () {
            span.closest(".modal").style.display = "none";
        });
    });

    // Close modals on click outside
    window.addEventListener("click", function (event) {
        [postModal, photoModal, videoModal, articleModal].forEach(modal => {
            if (event.target === modal) modal.style.display = "none";
        });
    });
});
