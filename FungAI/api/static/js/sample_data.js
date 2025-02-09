const fungalTypeMapping = {
    "IBT_23255": "IBT 26955",
    "IBT_32802": "IBT 41508"
};

async function fetchSampleData(fungalType) {
    try {
        const response = await fetch(`/sample-data/?fungal_type=${fungalType}`);
        const data = await response.json();

        if (data.files) {
            // Update the modal title dynamically using the mapping
            const modalTitleSpan = document.getElementById("ibt-number");
            const displayName = fungalTypeMapping[fungalType] || fungalType; // Default to fungalType if no mapping exists
            modalTitleSpan.textContent = displayName;

            // Populate the sample grid with the fetched data
            const grid = document.getElementById("sample-grid");
            grid.innerHTML = "";

            data.files.forEach((file) => {
                const col = document.createElement("div");
                col.className = "col-md-3 mb-3";
                col.innerHTML = `
                    <div class="card">
                        <img src="/static/images/sample_data/${fungalType}/${file}" class="card-img-top" alt="${file}">
                        <div class="card-body text-center">
                            <input type="checkbox" class="sample-checkbox" data-file="${file}" data-type="${fungalType}">
                            <label>${file}</label>
                        </div>
                    </div>
                `;
                grid.appendChild(col);
            });

            // Show the modal
            $("#sampleDataModal").modal("show");
        } else {
            alert("No files found for this category.");
        }
    } catch (error) {
        console.error("Error fetching sample data:", error);
    }
}


document.getElementById("select-all").addEventListener("click", () => {
    const checkboxes = document.querySelectorAll(".sample-checkbox");
    checkboxes.forEach((checkbox) => {
        checkbox.checked = true;
    });
});

document.getElementById("download-selected").addEventListener("click", async () => {
    const checkboxes = document.querySelectorAll(".sample-checkbox:checked");
    if (checkboxes.length === 0) {
        alert("Please select at least one file to download.");
        return;
    }

    if (checkboxes.length === 1) {
        const file = checkboxes[0].getAttribute("data-file");
        const fungalType = checkboxes[0].getAttribute("data-type");
        const link = document.createElement("a");
        link.href = `/download/${fungalType}/${file}`;
        link.download = file;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } else {
        const files = Array.from(checkboxes).map((checkbox) => checkbox.getAttribute("data-file"));
        const fungalType = checkboxes[0].getAttribute("data-type");
        const queryParams = new URLSearchParams({ fungal_type: fungalType, files: files.join(",") });

        const link = document.createElement("a");
        link.href = `/download/?${queryParams}`;
        link.download = "selected_images.zip";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
});
