import { GetDarkMode, SetDarkMode } from "./wailsjs/go/app/App";

// when domcontentloaded, check if dark mode is enabled
export const InitialiseDarkModeConfig = async (): Promise<void> => {
    // from https://flowbite.com/docs/customize/dark-mode/#content
    const themeToggleDarkIcon = document.getElementById("theme-toggle-dark-icon") as HTMLElement;
    const themeToggleLightIcon = document.getElementById("theme-toggle-light-icon") as HTMLElement;
    const themeToggleBtnText = document.getElementById("theme-toggle-text") as HTMLElement;
    if (!themeToggleDarkIcon || !themeToggleLightIcon || !themeToggleBtnText) {
        throw new Error("Could not find theme toggle button elements");
    }

    // Find a style element containing @sweetalert2/theme-dark/dark.css
    let swalDarkStyleEl: HTMLStyleElement | null = null;
    let swalDefaultStyleEl: HTMLStyleElement | null = null;
    const styleElements = document.head.getElementsByTagName("style");
    for (const styleElement of styleElements) {
        const attributes = styleElement.attributes;
        for (const attribute of attributes) {
            const value = attribute.value;
            if (value.includes("@sweetalert2/theme-dark/dark.css")) {
                swalDarkStyleEl = styleElement;
                break;
            }

            if (value.includes("@sweetalert2/theme-default/default.css")) {
                swalDefaultStyleEl = styleElement;
                break;
            }
        }

        if (swalDarkStyleEl && swalDefaultStyleEl) {
            break;
        }
    }
    if (!swalDarkStyleEl || !swalDefaultStyleEl) {
        throw new Error("Could not find sweetalert2 style elements");
    }

    // Change the icons inside the button based on previous settings
    const isDarkMode = await GetDarkMode();
    if (isDarkMode) {
        themeToggleLightIcon.classList.remove("hidden");
        themeToggleBtnText.textContent = "Light Mode";
        document.documentElement.classList.add("dark");
        swalDarkStyleEl.disabled = false;
        swalDefaultStyleEl.disabled = true;
    } else {
        themeToggleDarkIcon.classList.remove("hidden");
        themeToggleBtnText.textContent = "Dark Mode";
        document.documentElement.classList.remove("dark");
        swalDarkStyleEl.disabled = true;
        swalDefaultStyleEl.disabled = false;
    }

    const themeToggleBtn = document.getElementById("theme-toggle") as HTMLElement;
    if (!themeToggleBtn) {
        throw new Error("Could not find theme toggle button");
    }

    // Initialise again to avoid null errors
    const swalDarkStyleElement = swalDarkStyleEl;
    const swalDefaultStyleElement = swalDefaultStyleEl;

    themeToggleBtn.addEventListener("click", async () => {
        // toggle icons inside button
        themeToggleDarkIcon.classList.toggle("hidden");
        themeToggleLightIcon.classList.toggle("hidden");

        if (document.documentElement.classList.contains("dark")) {
            document.documentElement.classList.remove("dark");
            themeToggleBtnText.textContent = "Dark Mode";
            swalDarkStyleElement.disabled = true;
            swalDefaultStyleElement.disabled = false;
            await SetDarkMode(false);
            return;
        } 
        document.documentElement.classList.add("dark");
        themeToggleBtnText.textContent = "Light Mode";

        swalDarkStyleElement.disabled = false;
        swalDefaultStyleElement.disabled = true;
        await SetDarkMode(true);
    });
};
