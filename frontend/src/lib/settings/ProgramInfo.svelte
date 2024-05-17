<script lang="ts">
    import { Helper, Hr } from "flowbite-svelte";
    import { GetProgramInfo, CheckForUpdates } from "../../scripts/wailsjs/go/app/App";
    import { onMount } from "svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { EN, GetCachedLanguage, JP, translateText } from "../../scripts/language";

    let programVer: string;
    let programLogicVer: string;

    export let lastSavedUpdateStr: Record<string, string>;
    const language = GetCachedLanguage();

    onMount(async() => {
        const programInfo = await GetProgramInfo();
        programVer = programInfo.ProgramVer;
        programLogicVer = programInfo.BackendVer;

        const checkingForUpdates = await translateText("Checking for updates...");
        const checkForUpdates = await translateText("Check for updates");
        const outdatedLastCheckedEn = await translateText("Outdated, last checked at", EN);
        const outdatedLastCheckedJp = await translateText("Outdated, last checked at", JP);
        const upToDateLastCheckedEn = await translateText("Up-to-date, last checked at", EN);
        const upToDateLastCheckedJp = await translateText("Up-to-date, last checked at", JP);

        const latestVer = document.getElementById("latest-ver") as HTMLElement;
        if (lastSavedUpdateStr[language] === undefined) {
            lastSavedUpdateStr = {
                [EN]: "Unknown", 
                [JP]: "最新の情報はありません",
            };
        }
        latestVer.innerText = lastSavedUpdateStr[language];

        const updateBtn = document.getElementById("update-btn") as HTMLButtonElement;
        const updateBtnText = updateBtn.querySelector("span") as HTMLElement;
        updateBtnText.innerText = checkForUpdates;
        const updateBtnIcon = updateBtn.querySelector("svg") as unknown as SVGAElement;
        updateBtn.addEventListener("click", async() => {
            updateBtn.disabled = true;
            updateBtnIcon.classList.add("animate-spin");
            updateBtnText.innerText = checkingForUpdates;

            const outdated = await CheckForUpdates();
            const currentTime = new Date().toLocaleTimeString();
            if (outdated) {
                lastSavedUpdateStr = {
                    [EN]: outdatedLastCheckedEn + currentTime,
                    [JP]: outdatedLastCheckedJp + currentTime,
                }
            } else {
                lastSavedUpdateStr = {
                    [EN]: upToDateLastCheckedEn + currentTime,
                    [JP]: upToDateLastCheckedJp + currentTime,
                }
            }
            latestVer.innerText = lastSavedUpdateStr[language];

            updateBtn.disabled = false;
            updateBtnIcon.classList.remove("animate-spin");
            updateBtnText.innerText = checkForUpdates;
        });
    });

    let devNote1Part1: string;
    let devNote1Part3: string;

    let devNote2Part1: string;
    let devNote2Part2: string;
    let devNote2Part3: string;
    let devNote2Part4: string;
    let devNote2Part5: string;
    if (language === EN) {
        devNote1Part1 = "If you like using Cultured Downloader, please consider giving it a star on";
        devNote1Part3 = "if you haven't already!";

        devNote2Part1 = "Additionally, please consider supporting this project by";
        devNote2Part2 = "buying me a coffee";
        devNote2Part3 = "or"
        devNote2Part4 = "sponsoring me";
        devNote2Part5 = " via GitHub sponsors! Your contribution would help ensure the sustainability of this project. Thank you for reading <3";
    } else {
        devNote1Part1 = "Cultured Downloaderをご利用いただき、ありがとうございます。もしまだであれば、";
        devNote1Part3 = "でスターを付けていただけると嬉しいです！";

        devNote2Part1 = "このプロジェクトのサポートを検討していただき、ありがとうございます。こちらから";
        devNote2Part2 = "コーヒーをご購入";
        devNote2Part3 = "いただくか、";
        devNote2Part4 = "GitHubスポンサー";
        devNote2Part5 = "としてサポートすることができます。皆様の貢献は、このプロジェクトの持続可能性を確保するのに役立ちます。お読みいただき、ありがとうございます。<3";
    }
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
        - {devNote1Part1}
        <button class="btn-link text-left" on:click={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader")}>GitHub</button>
        {devNote1Part3}
    </Helper>
    <Helper id="devNote2">
        - {devNote2Part1}
        <button on:click={() => BrowserOpenURL("https://ko-fi.com/dratornic")} class="btn-link text-left">{devNote2Part2}</button>
        {devNote2Part3}
        <button on:click={() => BrowserOpenURL("https://github.com/sponsors/KJHJason")} class="btn-link text-left">{devNote2Part4}</button>
        {devNote2Part5}
    </Helper>
    <button class="mt-2 ms-auto flex btn btn-success items-center" id="update-btn">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="shrink-0 w-4 h-4 me-2" role="img" aria-label="update solid" viewBox="0 0 122.61 122.88">
            <path d="M111.9,61.57a5.36,5.36,0,0,1,10.71,0A61.3,61.3,0,0,1,17.54,104.48v12.35a5.36,5.36,0,0,1-10.72,0V89.31A5.36,5.36,0,0,1,12.18,84H40a5.36,5.36,0,1,1,0,10.71H23a50.6,50.6,0,0,0,88.87-33.1ZM106.6,5.36a5.36,5.36,0,1,1,10.71,0V33.14A5.36,5.36,0,0,1,112,38.49H84.44a5.36,5.36,0,1,1,0-10.71H99A50.6,50.6,0,0,0,10.71,61.57,5.36,5.36,0,1,1,0,61.57,61.31,61.31,0,0,1,91.07,8,61.83,61.83,0,0,1,106.6,20.27V5.36Z"/>
        </svg>
        <span>Check for updates</span>
    </button>
</div>

