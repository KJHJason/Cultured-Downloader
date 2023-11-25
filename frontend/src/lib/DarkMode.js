// from https://flowbite.com/docs/customize/dark-mode/#content
const themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon");
const themeToggleLightIcon = document.getElementById("theme-toggle-light-icon");
const themeToggleBtnText = document.getElementById("theme-toggle-text");

// Change the icons inside the button based on previous settings
if (localStorage.getItem("color-theme") === "dark" || (!("color-theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    themeToggleLightIcon.classList.remove("hidden");
    themeToggleBtnText.textContent = "Light Mode";
} else {
    themeToggleDarkIcon.classList.remove("hidden");
    themeToggleBtnText.textContent = "Dark Mode";
}

const themeToggleBtn = document.getElementById("theme-toggle");

themeToggleBtn.addEventListener("click", () => {
    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle("hidden");
    themeToggleLightIcon.classList.toggle("hidden");

    // if set via local storage previously
    if (localStorage.getItem("color-theme")) {
        if (localStorage.getItem("color-theme") === "light") {
            document.documentElement.classList.add("dark");
            themeToggleBtnText.textContent = "Light Mode";
            localStorage.setItem("color-theme", "dark");
        } else {
            document.documentElement.classList.remove("dark");
            themeToggleBtnText.textContent = "Dark Mode";
            localStorage.setItem("color-theme", "light");
        }

    // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains("dark")) {
            document.documentElement.classList.remove("dark");
            themeToggleBtnText.textContent = "Dark Mode";
            localStorage.setItem("color-theme", "light");
        } else {
            document.documentElement.classList.add("dark");
            themeToggleBtnText.textContent = "Light Mode";
            localStorage.setItem("color-theme", "dark");
        }
    }
});
