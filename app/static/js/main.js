const menuToggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".site-navigation");

if (menuToggle && navigation) {
    menuToggle.addEventListener("click", () => {
        const isOpen = navigation.classList.toggle("is-open");

        menuToggle.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );

        menuToggle.textContent = isOpen ? "CLOSE" : "MENU";
    });
}

document.querySelectorAll(".video-thumbnail").forEach((button) => {
    button.addEventListener("click", () => {
        const videoId = button.dataset.youtubeId;

        if (!videoId) {
            return;
        }

        const iframe = document.createElement("iframe");

        iframe.className = "video-embed";
        iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`;
        iframe.title = "YouTube video player";
        iframe.allow =
            "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
        iframe.allowFullscreen = true;

        button.replaceWith(iframe);
    });
});

const photoLightbox = document.querySelector("#photo-lightbox");

if (photoLightbox) {
    const lightboxImage = photoLightbox.querySelector(
        ".photo-lightbox-image"
    );

    const lightboxTitle = photoLightbox.querySelector(
        ".photo-lightbox-title"
    );

    const lightboxCredit = photoLightbox.querySelector(
        ".photo-lightbox-credit"
    );

    const closeButton = photoLightbox.querySelector(
        ".photo-lightbox-close"
    );

    const closeLightbox = () => {
        photoLightbox.hidden = true;
        lightboxImage.src = "";
        document.body.style.overflow = "";
    };

    document.querySelectorAll(".photo-thumbnail").forEach((button) => {
        button.addEventListener("click", () => {
            lightboxImage.src = button.dataset.photoSrc;
            lightboxImage.alt = button.dataset.photoTitle || "Demo Band photo";

            lightboxTitle.textContent =
                button.dataset.photoTitle || "";

            lightboxCredit.textContent =
                button.dataset.photoCredit
                    ? `Photo: ${button.dataset.photoCredit}`
                    : "";

            photoLightbox.hidden = false;
            document.body.style.overflow = "hidden";
        });
    });

    closeButton.addEventListener("click", closeLightbox);

    photoLightbox.addEventListener("click", (event) => {
        if (event.target === photoLightbox) {
            closeLightbox();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (
            event.key === "Escape"
            && !photoLightbox.hidden
        ) {
            closeLightbox();
        }
    });
}