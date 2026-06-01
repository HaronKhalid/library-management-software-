/* main.js - Core UI Interactivity Script */
document.addEventListener("DOMContentLoaded", () => {
    // Theme Switcher Logic
    const themeToggleBtn = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const themeText = document.getElementById("theme-text");
    
    // Check local storage or default to dark
    const currentTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", currentTheme);
    updateThemeUI(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const activeTheme = document.documentElement.getAttribute("data-theme");
            const newTheme = activeTheme === "dark" ? "light" : "dark";
            
            document.documentElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateThemeUI(newTheme);
        });
    }

    function updateThemeUI(theme) {
        if (!themeIcon || !themeText) return;
        if (theme === "light") {
            themeIcon.className = "lucide-sun";
            themeIcon.textContent = "☀️";
            themeText.textContent = "Light Mode";
        } else {
            themeIcon.className = "lucide-moon";
            themeIcon.textContent = "🌙";
            themeText.textContent = "Dark Mode";
        }
    }

    // Dismiss Flash Alerts
    const closeButtons = document.querySelectorAll(".alert-close");
    closeButtons.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const alertElement = e.currentTarget.closest(".alert");
            if (alertElement) {
                alertElement.style.opacity = "0";
                alertElement.style.transform = "translateY(-10px)";
                alertElement.style.transition = "opacity 0.3s ease, transform 0.3s ease";
                setTimeout(() => alertElement.remove(), 300);
            }
        });
    });

    // Automatically fade out success alerts after 5 seconds
    const autoDismissAlerts = document.querySelectorAll(".alert-success, .alert-info");
    autoDismissAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            alert.style.transition = "opacity 0.3s ease, transform 0.3s ease";
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Tab Interface Logic (For Members/Librarians tabs)
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetPaneId = btn.getAttribute("data-target");
            
            tabButtons.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(pane => pane.classList.remove("active"));
            
            btn.classList.add("active");
            const targetPane = document.getElementById(targetPaneId);
            if (targetPane) {
                targetPane.classList.add("active");
            }
        });
    });
});
