const linkId = "swal-theme-link";
export const ToggleCSSThemes = (isDarkMode: boolean): void => {
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
