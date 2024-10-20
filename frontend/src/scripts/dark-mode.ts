import { GetDarkMode, SetDarkMode } from "./wailsjs/go/app/App";

// https://github.com/probablykasper/date-picker-svelte
const ToggleDatePickerCssProperties = (isDarkMode: boolean): void => {
    if (isDarkMode) {
        document.documentElement.style.setProperty("--date-picker-background", "#27272a");
        document.documentElement.style.setProperty("--date-picker-foreground", "#f7f7f7");
    } else {
        document.documentElement.style.setProperty("--date-picker-background", "#fff");
        document.documentElement.style.setProperty("--date-picker-foreground", "#000");
    }
};

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
};

// when domcontentloaded, check if dark mode is enabled
export const InitialiseDarkModeConfig = async (): Promise<void> => {
    // from https://flowbite.com/docs/customize/dark-mode/#content
    const themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon") as HTMLElement;
    const themeToggleLightIcon = document.getElementById("theme-toggle-light-icon") as HTMLElement;
    const darkModeToggleTxt = document.getElementById("dark-mode-toggle-text") as HTMLElement;
    const lightModeToggleTxt = document.getElementById("light-mode-toggle-text") as HTMLElement;
    if (!themeToggleDarkIcon || !themeToggleLightIcon || !darkModeToggleTxt || !lightModeToggleTxt) {
        throw new Error("Could not find theme toggle button elements");
    }

    const toggleToggleText = (isDarkMode: boolean): void => {
        if (isDarkMode) {
            themeToggleLightIcon.classList.remove("hidden");
            document.documentElement.classList.add("dark");

            darkModeToggleTxt.classList.add("hidden");
            darkModeToggleTxt.ariaHidden = "true";

            lightModeToggleTxt.classList.remove("hidden");
            lightModeToggleTxt.ariaHidden = "false";
            return;
        } 

        themeToggleDarkIcon.classList.remove("hidden");
        document.documentElement.classList.remove("dark");

        darkModeToggleTxt.classList.remove("hidden");
        darkModeToggleTxt.ariaHidden = "false";

        lightModeToggleTxt.classList.add("hidden");
        lightModeToggleTxt.ariaHidden = "true";
    };

    // Change the icons inside the button based on previous settings
    const isDarkMode = await GetDarkMode();
    toggleToggleText(isDarkMode);
    ToggleCSSThemes(isDarkMode)
    ToggleDatePickerCssProperties(isDarkMode);

    const themeToggleBtn = document.getElementById("theme-toggle") as HTMLElement;
    if (!themeToggleBtn) {
        throw new Error("Could not find theme toggle button");
    }

    themeToggleBtn.addEventListener("click", async () => {
        // toggle icons inside button
        themeToggleDarkIcon.classList.toggle("hidden");
        themeToggleLightIcon.classList.toggle("hidden");

        const isCurrentlyDarkMode = document.documentElement.classList.contains("dark");
        toggleToggleText(!isCurrentlyDarkMode);
        ToggleCSSThemes(!isCurrentlyDarkMode);
        ToggleDatePickerCssProperties(isDarkMode);
        await SetDarkMode(!isCurrentlyDarkMode);
    });
};
