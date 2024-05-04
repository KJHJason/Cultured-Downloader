import { GetDarkMode, SetDarkMode } from "./wailsjs/go/app/App";

const linkId = "swal-theme-link";
const ToggleCSSThemes = (isDarkMode: boolean): void => {
    const existingLink = document.getElementById(linkId);
    if (existingLink) {
        existingLink.remove();
    }

    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.id = linkId;

    // Note: Using cdn instead of using imports via node.js due to how wails compiles the frontend assets in production env
    if (isDarkMode) {
        link.href = "https://cdn.jsdelivr.net/npm/@sweetalert2/theme-dark@latest/dark.css";
    } else {
        link.href = "https://cdn.jsdelivr.net/npm/@sweetalert2/theme-default@latest/default.css";
    }
    document.head.appendChild(link);
}

// when domcontentloaded, check if dark mode is enabled
export const InitialiseDarkModeConfig = async (): Promise<void> => {
    // from https://flowbite.com/docs/customize/dark-mode/#content
    const themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon") as HTMLElement;
    const themeToggleLightIcon = document.getElementById("theme-toggle-light-icon") as HTMLElement;
    const themeToggleBtnText = document.getElementById("theme-toggle-text") as HTMLElement;
    if (!themeToggleDarkIcon || !themeToggleLightIcon || !themeToggleBtnText) {
        throw new Error("Could not find theme toggle button elements");
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
    ToggleCSSThemes(isDarkMode)

    const themeToggleBtn = document.getElementById("theme-toggle") as HTMLElement;
    if (!themeToggleBtn) {
        throw new Error("Could not find theme toggle button");
    }

    themeToggleBtn.addEventListener("click", async () => {
        // toggle icons inside button
        themeToggleDarkIcon.classList.toggle("hidden");
        themeToggleLightIcon.classList.toggle("hidden");

        const isCurrentlyDarkMode = document.documentElement.classList.contains("dark");
        if (isCurrentlyDarkMode) {
            document.documentElement.classList.remove("dark");
            themeToggleBtnText.textContent = "Dark Mode"; // text for the user to change back to dark mode
        } else {
            document.documentElement.classList.add("dark");
            themeToggleBtnText.textContent = "Light Mode"; // text for the user to change back to light mode
        }
        ToggleCSSThemes(!isCurrentlyDarkMode);
        await SetDarkMode(!isCurrentlyDarkMode);
    });
};
