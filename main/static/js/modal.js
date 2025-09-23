document.addEventListener("DOMContentLoaded", function () {
    // ---- Post Modal ----
    const postModal = document.getElementById("postModal");
    const startBtn = document.querySelector(".start-a-post");

    if (postModal && startBtn) {
        startBtn.addEventListener("click", () => {
            postModal.style.display = "block";
        });
    }

    // Close post modal
    const closePostBtn = postModal.querySelector(".close");
    closePostBtn.addEventListener("click", () => {
        postModal.style.display = "none";
    });

    // Close on outside click
    window.addEventListener("click", (e) => {
        if (e.target === postModal) postModal.style.display = "none";
    });

    // ---- Post Modals ----
    const postModals = {
        post: document.getElementById("postModal"),
        photo: document.getElementById("photoModal"),
        video: document.getElementById("videoModal"),
        article: document.getElementById("articleModal")
    };

    const postButtons = {
        start: document.querySelector(".start-a-post"),
        photo: document.querySelector("button:has(i.fa-image)"),
        video: document.querySelector("button:has(i.fa-video)"),
        article: document.querySelector("button:has(i.fa-newspaper)")
    };

    // Open post modals
    Object.keys(postButtons).forEach(key => {
        if (postButtons[key] && postModals[key]) {
            postButtons[key].addEventListener("click", () => {
                postModals[key].style.display = "block";
            });
        }
    });

    // ---- Experience Modal ----
    const expModal = document.getElementById("experienceModal");
    const addExpBtn = document.getElementById("addExperienceBtn");
    if (expModal && addExpBtn) {
        const closeExpBtn = expModal.querySelector(".close");
        addExpBtn.addEventListener("click", () => expModal.style.display = "block");
        closeExpBtn.addEventListener("click", () => expModal.style.display = "none");
        window.addEventListener("click", (e) => {
            if (e.target === expModal) expModal.style.display = "none";
        });
    }

    // ---- Close buttons for all post modals ----
    document.querySelectorAll(".close").forEach(span => {
        span.addEventListener("click", () => {
            const modal = span.closest(".modal");
            if (modal) modal.style.display = "none";
        });
    });

    // ---- Close post modals on outside click ----
    window.addEventListener("click", (event) => {
        Object.values(postModals).forEach(modal => {
            if (event.target === modal) modal.style.display = "none";
        });
    });
});

