/* ===== BUILD MASONRY COLUMNS (round-robin = folder order preserved) ===== */
const cols = [
    document.getElementById("mCol0"),
    document.getElementById("mCol1"),
    document.getElementById("mCol2")
];
const source = document.getElementById("gallerySource");
const orderedItems = Array.from(source.querySelectorAll(".gallery-item"));

orderedItems.forEach((item, i) => {
    cols[i % 3].appendChild(item);
});

/* ===== LIGHTBOX ===== */
const lightbox = document.getElementById("lightbox");
const lightboxImage = document.getElementById("lightboxImage");
const closeBtn = document.querySelector(".lightbox-close");
const prevImgBtn = document.querySelector(".lightbox-nav.prev");
const nextImgBtn = document.querySelector(".lightbox-nav.next");

let currentImageIndex = 0;

function openLightbox(index) {
    currentImageIndex = index;
    lightbox.style.display = "flex";
    updateLightbox();
}

function updateLightbox() {
    const img = orderedItems[currentImageIndex].querySelector("img");
    lightboxImage.src = img.src;
}

function closeLightbox() {
    lightbox.style.display = "none";
}

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % orderedItems.length;
    updateLightbox();
}

function prevImage() {
    currentImageIndex =
        (currentImageIndex - 1 + orderedItems.length) % orderedItems.length;
    updateLightbox();
}

/* ===== EVENTS ===== */
orderedItems.forEach((item, i) => {
    item.addEventListener("click", () => openLightbox(i));
});

closeBtn.onclick = closeLightbox;
nextImgBtn.onclick = nextImage;
prevImgBtn.onclick = prevImage;

document.addEventListener("keydown", e => {
    if (lightbox.style.display !== "flex") return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") nextImage();
    if (e.key === "ArrowLeft") prevImage();
});

