import { GetDarkMode, SetDarkMode } from "./wailsjs/go/app/App";

// when domcontentloaded, check if dark mode is enabled
document.addEventListener("DOMContentLoaded", async () => {
    // from https://flowbite.com/docs/customize/dark-mode/#content
    const themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon") as HTMLElement;
    const themeToggleLightIcon = document.getElementById("theme-toggle-light-icon") as HTMLElement;
    const themeToggleBtnText = document.getElementById("theme-toggle-text") as HTMLElement;
    if (!themeToggleDarkIcon || !themeToggleLightIcon || !themeToggleBtnText) {
        return;
    }

    // Change the icons inside the button based on previous settings
    const isDarkMode = await GetDarkMode();
    if (isDarkMode) {
        themeToggleLightIcon.classList.remove("hidden");
        themeToggleBtnText.textContent = "Light Mode";
        document.documentElement.classList.add("dark");
    } else {
        themeToggleDarkIcon.classList.remove("hidden");
        themeToggleBtnText.textContent = "Dark Mode";
        document.documentElement.classList.remove("dark");
    }

    const themeToggleBtn = document.getElementById("theme-toggle") as HTMLElement;
    if (!themeToggleBtn) {
        return;
    }

    themeToggleBtn.addEventListener("click", async () => {
        // toggle icons inside button
        themeToggleDarkIcon.classList.toggle("hidden");
        themeToggleLightIcon.classList.toggle("hidden");

        if (document.documentElement.classList.contains("dark")) {
            document.documentElement.classList.remove("dark");
            themeToggleBtnText.textContent = "Dark Mode";
            await SetDarkMode(false);
            return;
        } 
        document.documentElement.classList.add("dark");
        themeToggleBtnText.textContent = "Light Mode";
        await SetDarkMode(true);
    });
});
