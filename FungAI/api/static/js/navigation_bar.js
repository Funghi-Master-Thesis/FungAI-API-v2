document.addEventListener("DOMContentLoaded", function () {
    const tabLinks = document.querySelectorAll('.nav-tabs .nav-link');
    const fungaiForm = document.querySelector('#fungai form');

    // Add event listener to the FungAI form
    if (fungaiForm) {
        fungaiForm.addEventListener('submit', function () {
            const activeTab = document.querySelector('.nav-tabs .nav-link.active');
            if (activeTab) {
                const activeTabId = activeTab.getAttribute('href');
                localStorage.setItem("activeTab", activeTabId);
            }
        });
    }

    // Set the active tab after reload
    const activeTabId = localStorage.getItem("activeTab");
    if (activeTabId) {
        tabLinks.forEach(tab => tab.classList.remove('active'));
        const tabPanes = document.querySelectorAll('.tab-pane');
        tabPanes.forEach(pane => pane.classList.remove('active', 'show'));

        const activeTab = document.querySelector(`.nav-tabs .nav-link[href="${activeTabId}"]`);
        const activeTabPane = document.querySelector(activeTabId);

        if (activeTab && activeTabPane) {
            activeTab.classList.add('active');
            activeTabPane.classList.add('active', 'show');
        }

        localStorage.removeItem("activeTab");
    }
});
