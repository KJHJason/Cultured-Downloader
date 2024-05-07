<script lang="ts">
    import { Helper, Hr } from "flowbite-svelte";
    import { GetProgramInfo, CheckForUpdates } from "../../scripts/wailsjs/go/app/App";
    import { onMount } from "svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";

    let programVer: string;
    let programLogicVer: string;
    export let lastSavedUpdateStr: string;

    onMount(async() => {
        const programInfo = await GetProgramInfo();
        programVer = programInfo.ProgramVer;
        programLogicVer = programInfo.BackendVer;

        const latestVer = document.getElementById("latest-ver") as HTMLElement;
        if (lastSavedUpdateStr === "") {
            lastSavedUpdateStr = "Unknown";
        }
        latestVer.innerText = lastSavedUpdateStr;

        const updateBtn = document.getElementById("update-btn") as HTMLButtonElement;
        const updateBtnText = updateBtn.querySelector("span") as HTMLElement;
        const updateBtnIcon = updateBtn.querySelector("svg") as unknown as SVGAElement;
        updateBtn.addEventListener("click", async() => {
            updateBtn.disabled = true;
            updateBtnIcon.classList.add("animate-spin");
            updateBtnText.innerText = "Checking for updates...";

            const outdated = await CheckForUpdates();
            const currentTime = new Date();
            if (outdated) {
                lastSavedUpdateStr = `Outdated, last checked at ${currentTime.toLocaleTimeString()}`;
            } else {
                lastSavedUpdateStr = `Up-to-date, last checked at ${currentTime.toLocaleTimeString()}`
            }
            latestVer.innerText = lastSavedUpdateStr;

            updateBtn.disabled = false;
            updateBtnIcon.classList.remove("animate-spin");
            updateBtnText.innerText = "Check for updates";
        });
    });
</script>

<h4 class="my-0">Cultured Downloader</h4>
<p>
    Version {programVer} by 
    <button class="btn-link text-left" on:click={() => BrowserOpenURL("https://github.com/KJHJason")}>KJHJason</button>
</p>
<p>
    Repository: 
    <button class="btn-link text-left" on:click={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader")}>https://github.com/KJHJason/Cultured-Downloader</button>
</p>
<p>
    Latest version: <span id="latest-ver">Unknown</span>
</p>
<Hr />
<h4>Cultured Downloader Logic</h4>
<p>
    Version {programLogicVer} by 
    <button class="btn-link text-left" on:click={() => BrowserOpenURL("https://github.com/KJHJason")}>KJHJason</button>
</p>
<p>
    Repository: 
    <button class="btn-link text-left" on:click={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader-Logic")}>https://github.com/KJHJason/Cultured-Downloader-Logic</button>
</p>
<Hr />

<div class="w-full">
    <Helper>Developer's note:</Helper>
    <Helper>
        Please consider supporting this project by 
        <button on:click={() => BrowserOpenURL("https://ko-fi.com/dratornic")} class="btn-link text-left">buying me a coffee</button> 
        or 
        <button on:click={() => BrowserOpenURL("https://github.com/sponsors/KJHJason")} class="btn-link text-left">sponsoring me</button>! 
        Your contribution would help ensure the sustainability of this project. Thank you for reading &lt;3
    </Helper>
    <button class="mt-2 ms-auto flex btn btn-success items-center" id="update-btn">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="shrink-0 w-4 h-4 me-2" role="img" aria-label="update solid" viewBox="0 0 122.61 122.88">
            <path d="M111.9,61.57a5.36,5.36,0,0,1,10.71,0A61.3,61.3,0,0,1,17.54,104.48v12.35a5.36,5.36,0,0,1-10.72,0V89.31A5.36,5.36,0,0,1,12.18,84H40a5.36,5.36,0,1,1,0,10.71H23a50.6,50.6,0,0,0,88.87-33.1ZM106.6,5.36a5.36,5.36,0,1,1,10.71,0V33.14A5.36,5.36,0,0,1,112,38.49H84.44a5.36,5.36,0,1,1,0-10.71H99A50.6,50.6,0,0,0,10.71,61.57,5.36,5.36,0,1,1,0,61.57,61.31,61.31,0,0,1,91.07,8,61.83,61.83,0,0,1,106.6,20.27V5.36Z"/>
        </svg>
        <span>Check for updates</span>
    </button>
</div>

