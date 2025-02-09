document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll(".info-item img");
    const modal = document.getElementById("imageModal");
    const modalImage = document.getElementById("modalImage");

    images.forEach((image) => {
        image.addEventListener("click", () => {
            modalImage.src = image.src; // Set the modal image source to the clicked image
            $(modal).modal("show"); // Show the modal
        });
    });

    // Clear the modal image source on close to ensure no flickering
    $(modal).on("hidden.bs.modal", () => {
        modalImage.src = "";
    });
});
