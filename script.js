console.log("JS loaded.");

// Load mode
let currentTheme = localStorage.getItem("theme") || "light";
document.documentElement.setAttribute("data-theme", currentTheme);

// Toggle theme (click and keyboard accessible)
const toggle = document.getElementById("theme-toggle");
if (toggle) {
    toggle.setAttribute("aria-label", "Toggle theme");
    const toggleTheme = () => {
        const newTheme = document.documentElement.getAttribute("data-theme") === "light" 
            ? "dark" 
            : "light";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    };

    toggle.addEventListener("click", toggleTheme);
    toggle.addEventListener("keydown", (e) => { if (e.key === 'Enter' || e.key === ' ') toggleTheme(); });
}
