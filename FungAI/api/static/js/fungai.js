document.addEventListener("DOMContentLoaded", () => {
    // Trigger file picker when custom button is clicked
    document.getElementById("custom-file-button").addEventListener("click", function () {
        document.getElementById("file-input").click(); // Simulate a click on the hidden file input
    });
    document.getElementById("custom-file-button-single").addEventListener("click", function () {
        document.getElementById("file-input-single").click(); // Simulate a click on the hidden file input
    });

    // Handle file selection
    document.getElementById("file-input").addEventListener("change", function (event) {
        const fileInput = event.target;
        const fileNameDisplay = document.getElementById("file-name");
        const filePreview = document.getElementById("file-preview");
        const clearFileButton = document.getElementById("clear-file-button");

        // Clear existing image preview
        filePreview.querySelectorAll("img").forEach((img) => img.remove());

        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];

            // Update file name
            fileNameDisplay.textContent = file.name;

            // Create and display image preview
            const imagePreview = document.createElement("img");
            imagePreview.src = URL.createObjectURL(file);
            filePreview.prepend(imagePreview);

            // Show the '×' button
            clearFileButton.style.display = "inline";
        } else {
            // Reset file name if no file is selected
            fileNameDisplay.textContent = "No file chosen";
            // Hide the '×' button
            clearFileButton.style.display = "none";
        }
    });

    document.getElementById("file-input-single").addEventListener("change", function (event) {
        const fileInput = event.target;
        const fileNameDisplay = document.getElementById("file-name-single");
        const filePreview = document.getElementById("file-preview-single");
        const clearFileButton = document.getElementById("clear-file-button-single");

        // Clear existing image preview
        filePreview.querySelectorAll("img").forEach((img) => img.remove());

        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];

            // Update file name
            fileNameDisplay.textContent = file.name;

            // Create and display image preview
            const imagePreview = document.createElement("img");
            imagePreview.src = URL.createObjectURL(file);
            filePreview.prepend(imagePreview);

            // Show the '×' button
            clearFileButton.style.display = "inline";
        } else {
            // Reset file name if no file is selected
            fileNameDisplay.textContent = "No file chosen";
            // Hide the '×' button
            clearFileButton.style.display = "none";
        }
    });

    // Add event listener to the '×' button
    document.getElementById("clear-file-button").addEventListener("click", function () {
        const fileInput = document.getElementById("file-input");
        const fileNameDisplay = document.getElementById("file-name");
        const filePreview = document.getElementById("file-preview");
        const clearFileButton = document.getElementById("clear-file-button");

        // Clear the file input
        fileInput.value = "";

        // Reset file name
        fileNameDisplay.textContent = "No file chosen";

        // Remove image preview
        filePreview.querySelectorAll("img").forEach((img) => img.remove());

        // Hide the '×' button
        clearFileButton.style.display = "none";
    });

    document.getElementById("clear-file-button-single").addEventListener("click", function () {
        const fileInput = document.getElementById("file-input-single");
        const fileNameDisplay = document.getElementById("file-name-single");
        const filePreview = document.getElementById("file-preview-single");
        const clearFileButton = document.getElementById("clear-file-button-single");

        // Clear the file input
        fileInput.value = "";

        // Reset file name
        fileNameDisplay.textContent = "No file chosen";

        // Remove image preview
        filePreview.querySelectorAll("img").forEach((img) => img.remove());

        // Hide the '×' button
        clearFileButton.style.display = "none";
    });

    // Handle upload button click
    document.getElementById("upload-button").addEventListener("click", async function (event) {
        event.preventDefault(); // Prevent form submission and page reload
        const form = document.getElementById("upload-form");
        const formData = new FormData(form);
        const fileInput = document.getElementById("file-input");
        const loadingSpinner = document.getElementById("loading-spinner");
        const resultsDiv = document.getElementById("prediction-results");

        if (!fileInput.files.length) {
            alert("Please select a file.");
            return;
        }

        // Show loading spinner and clear results
        loadingSpinner.style.display = "block";
        resultsDiv.innerHTML = "";

        try {
            const response = await fetch("/predict/", {
                method: "POST",
                body: formData,
            });

            if (response.status === 413) {
                alert("Error: File too large. Please upload a file smaller than 20 MB.");
                loadingSpinner.style.display = "none"; // Hide spinner
                return;
            }

            if (response.ok) {
                const data = await response.json();
                resultsDiv.innerHTML = `
                    <h3>Top Predictions:</h3>
                    <table class="prediction-table">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Genus</th>
                                <th>Species</th>
                                <th>Probability</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.predictions.map((pred, index) => `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${pred.class_name.split("-")[0]}</td>
                                    <td>${pred.class_name.split("-")[1]}</td>
                                    <td>${pred.probability.toFixed(2)}%</td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                `;
            } else {
                alert("Error: Unable to process the file.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("An error occurred. Please try again.");
        } finally {
            // Hide the loading spinner after processing
            loadingSpinner.style.display = "none";
        }
    });

    document.getElementById("upload-button-single").addEventListener("click", async function (event) {
        event.preventDefault(); // Prevent form submission and page reload
        const form = document.getElementById("upload-form-single");
        const formData = new FormData(form);
        const fileInput = document.getElementById("file-input-single");
        const loadingSpinner = document.getElementById("loading-spinner-single");
        const resultsDiv = document.getElementById("prediction-results-single");
    
        if (!fileInput.files.length) {
            alert("Please select a file.");
            return;
        }
    
        // Show loading spinner and clear results
        loadingSpinner.style.display = "block";
        resultsDiv.innerHTML = "";
    
        try {
            const response = await fetch("/predict_single/", {
                method: "POST",
                body: formData,
            });
    
            if (response.status === 413) {
                alert("Error: File too large. Please upload a file smaller than 20 MB.");
                loadingSpinner.style.display = "none"; // Hide spinner
                return;
            }
    
            if (response.ok) {
                const data = await response.json();
                resultsDiv.innerHTML = `
                    <h3>Top Predictions:</h3>
                    <table class="prediction-table-single">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Genus</th>
                                <th>Species</th>
                                <th>Probability</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.predictions.map((pred, index) => `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${pred.class_name.split("-")[0]}</td>
                                    <td>${pred.class_name.split("-")[1]}</td>
                                    <td>${pred.probability.toFixed(2)}%</td>
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                `;
            } else {
                alert("Error: Unable to process the file.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("An error occurred. Please try again.");
        } finally {
            // Hide the loading spinner after processing
            loadingSpinner.style.display = "none";
        }
    });
    
});

