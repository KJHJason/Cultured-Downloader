<script lang="ts">
    import { Helper, Hr } from "flowbite-svelte";
    import { GetProgramInfo, CheckForUpdates } from "../../scripts/wailsjs/go/app/App";
    import { onMount } from "svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { EN, GetCachedLanguage, JP, translate, translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";

    let programVer: string = $state("");
    let programLogicVer: string = $state("");

    interface Props {
        lastSavedUpdateStr: Record<string, string>;
    }

    let { lastSavedUpdateStr = $bindable() }: Props = $props();
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
                [EN]: await translateText("program_info_unknown", EN, "Unknown"), 
                [JP]: await translateText("program_info_unknown", JP, "最新の情報はありません"),
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
</script>

<h4 class="my-0">Cultured Downloader</h4>
<p>
    <Translate text="Version" /> {programVer} <Translate text="program_info_by" />
    <button class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason")}>KJHJason</button>
</p>
<p>
    <Translate text="Repository:" />
    <button class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader")}>https://github.com/KJHJason/Cultured-Downloader</button>
</p>
<p>
    <Translate text="Latest version:" /> <span id="latest-ver">Unknown</span>
</p>
<Hr />
<h4>Cultured Downloader Logic</h4>
<p>
    <Translate text="Version" /> {programLogicVer} <Translate text="program_info_by" />
    <button class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason")}>KJHJason</button>
</p>
<p>
    <Translate text="Repository:" />
    <button class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader-Logic")}>https://github.com/KJHJason/Cultured-Downloader-Logic</button>
</p>
<Hr />

<div class="w-full">
    <Helper>
        <Translate text="Developer's note:" />
    </Helper>
    <Helper>
        - <Translate text="If you like using Cultured Downloader, please consider giving it a star on" />
        <button class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader")}>GitHub</button>
        <Translate text="program_info_if you haven't already!" fallback="if you haven't already!" />
    </Helper>
    <Helper id="devNote2">
        - <Translate text="Additionally, please consider supporting this project by" />
        <button onclick={() => BrowserOpenURL("https://ko-fi.com/kjhjason")} class="btn-link text-left" id="ko-fi-btn">{translate("buying me a coffee", "ko-fi-btn")}</button>
        <Translate text="program_info_or" fallback="or" />
        <button onclick={() => BrowserOpenURL("https://github.com/sponsors/KJHJason")} class="btn-link text-left" id="github-sponsor-btn">{translate("program_info_sponsoring me", "github-sponsor-btn", "", "sponsoring me")}</button>
        <Translate text="via GitHub sponsors! Your contribution would help ensure the sustainability of this project. Thank you for reading <3" />
    </Helper>
    <button class="mt-2 ms-auto flex btn btn-success items-center" id="update-btn">
        <div class="text-main">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="shrink-0 w-4 h-4 me-2" role="img" aria-label="update solid" viewBox="0 0 122.61 122.88">
                <path d="M111.9,61.57a5.36,5.36,0,0,1,10.71,0A61.3,61.3,0,0,1,17.54,104.48v12.35a5.36,5.36,0,0,1-10.72,0V89.31A5.36,5.36,0,0,1,12.18,84H40a5.36,5.36,0,1,1,0,10.71H23a50.6,50.6,0,0,0,88.87-33.1ZM106.6,5.36a5.36,5.36,0,1,1,10.71,0V33.14A5.36,5.36,0,0,1,112,38.49H84.44a5.36,5.36,0,1,1,0-10.71H99A50.6,50.6,0,0,0,10.71,61.57,5.36,5.36,0,1,1,0,61.57,61.31,61.31,0,0,1,91.07,8,61.83,61.83,0,0,1,106.6,20.27V5.36Z"/>
            </svg>
        </div>
        <Translate text="check for updates" />
    </button>
</div>

