<script lang="ts">
    import { Tooltip, Toggle } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { GetPreferences, SetFantiaPreferences, SetGeneralPreferences } from "../../scripts/wailsjs/go/app/App";
    import { generalFormId, swal } from "../../scripts/constants";
    import { translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";
    import CacheDetails from "./CacheDetails.svelte";
    import { ArchiveSolid, InfoCircleSolid } from "flowbite-svelte-icons";
    import type { app } from "../../scripts/wailsjs/go/models";

    export let formId = generalFormId;
    export let promptSuccess: boolean;
    export let preferences: app.Preferences | undefined = undefined;

    export let showOrganisePostImagesInp: boolean = true;
    export let showDlGDriveInp: boolean = true;

    let cacheDetailsOpened = false;

    let DlPostThumbnailInp: HTMLInputElement;
    let DlPostImagesInp: HTMLInputElement;
    let OrganisePostImagesInp: HTMLInputElement;
    let DlPostAttachmentsInp: HTMLInputElement;
    let DlGDriveInp: HTMLInputElement;
    let OverwriteFilesInp: HTMLInputElement;
    let DetectOtherLinksInp: HTMLInputElement;
    let UseCacheDbInp: HTMLInputElement;

    let savedFantiaOrgImages: boolean;

    const processPrefs = (preferences: app.Preferences) => {
        DlPostThumbnailInp.checked   = preferences.DlPostThumbnail;
        DlPostImagesInp.checked      = preferences.DlPostImages;
        DlPostAttachmentsInp.checked = preferences.DlPostAttachments;
        OverwriteFilesInp.checked    = preferences.OverwriteFiles;
        DetectOtherLinksInp.checked  = preferences.DetectOtherLinks;
        UseCacheDbInp.checked        = preferences.UseCacheDb;

        if (showOrganisePostImagesInp) {
            savedFantiaOrgImages = preferences.OrganisePostImages;
            OrganisePostImagesInp.checked = preferences.OrganisePostImages;
        }
        if (showDlGDriveInp) {
            DlGDriveInp.checked = preferences.DlGDrive;
        }
    };

    onMount(async() => {
        DlPostThumbnailInp = document.getElementById("DlPostThumbnail") as HTMLInputElement;
        DlPostImagesInp = document.getElementById("DlPostImages") as HTMLInputElement;
        DlPostAttachmentsInp = document.getElementById("DlPostAttachments") as HTMLInputElement;
        OverwriteFilesInp = document.getElementById("OverwriteFiles") as HTMLInputElement;
        DetectOtherLinksInp = document.getElementById("DetectOtherLinks") as HTMLInputElement;
        UseCacheDbInp = document.getElementById("UseCacheDb") as HTMLInputElement;
        if (showOrganisePostImagesInp) {
            OrganisePostImagesInp = document.getElementById("OrganisePostImages") as HTMLInputElement;
        }
        if (showDlGDriveInp) {
            DlGDriveInp = document.getElementById("DlGDrive") as HTMLInputElement;
        }

        if (preferences === undefined) {
            preferences = await GetPreferences();
        }
        processPrefs(preferences);

        const success = await translateText("Success");
        const prefsSaved = await translateText("Preferences saved successfully");

        const prefForm = document.getElementById(formId) as HTMLFormElement;
        prefForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            if (preferences === undefined) {
                preferences = await GetPreferences();
            }

            const prefs: app.GeneralPreferences = {
                DlPostThumbnail:    DlPostThumbnailInp.checked,
                DlPostImages:       DlPostImagesInp.checked,
                DlPostAttachments:  DlPostAttachmentsInp.checked,
                OverwriteFiles:     OverwriteFilesInp.checked,
                DlGDrive:           false,
                DetectOtherLinks:   DetectOtherLinksInp.checked,
                UseCacheDb:         UseCacheDbInp.checked,
            };

            if (showDlGDriveInp) {
                prefs.DlGDrive = DlGDriveInp.checked;
            } else {
                prefs.DlGDrive = preferences.DlGDrive;
            }
            if (showOrganisePostImagesInp && savedFantiaOrgImages !== OrganisePostImagesInp.checked) {
                await SetFantiaPreferences({ OrganisePostImages: OrganisePostImagesInp.checked });
            }

            await SetGeneralPreferences(prefs);
            processPrefs(await GetPreferences());

            if (promptSuccess) {
                swal.fire({
                    title: success,
                    text: prefsSaved,
                    icon: "success",
                });
            }
        });
    });

    let organisePostImagesTooltip = "";
    let overwriteFilesTooltip = "";
    let detectOtherLinksTooltip = "";
    let useCacheDbTooltip = "";
    onMount(async () => {
        organisePostImagesTooltip = await translateText("Organise downloaded images into numbered folders and image files.");
        overwriteFilesTooltip = await translateText("This should not be turned on as the program will check the expected file size with your local/downloaded files and resume downloading if it's incomplete except for Pixiv Fanbox where it will skip if the file exists. Hence, this is not recommended unless you have corrupted files or incomplete Pixiv Fanbox files because your anti-virus software may flag the program as a ransomware!");
        detectOtherLinksTooltip = await translateText("Detects other URL(s) like MEGA and logs them in the respective post folder.");
        useCacheDbTooltip = await translateText("Store downloaded post URL(s) to prevent re-downloading the same post to speed up future downloads. You should only turn this off if you want to download the post again either due to updated content or downloading with a different settings like downloading GDrive links. Alternatively, you can manage the cache database by clicking the \"View Cache\" button below.");
    });
</script>

<form id={formId} class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
    <Toggle color="green" id="DlPostThumbnail" name="DlPostThumbnail">
        <Translate text="Download Post Thumbnail" />
    </Toggle>
    <Toggle color="green" id="DlPostImages" name="DlPostImages">
        <Translate text="Download Post Images" />
    </Toggle>
    <Toggle color="green" id="DlPostAttachments" name="DlPostAttachments">
        <Translate text="Download Post Attachments" />
    </Toggle>
    {#if showOrganisePostImagesInp}
        <Toggle color="green" id="OrganisePostImages" name="OrganisePostImages">
            <Translate text="Organise Post Images" />
            <button type="button" class="btn-text-link ml-2" id="organise-images-info">
                <InfoCircleSolid />
            </button>
            <Tooltip class="max-w-md" triggeredBy="#organise-images-info">
                {organisePostImagesTooltip}
            </Tooltip>
        </Toggle>
    {/if}
    {#if showDlGDriveInp}
        <Toggle color="green" id="DlGDrive" name="DlGDrive">
            <Translate text="Download GDrive Links" />
        </Toggle>
    {/if}
    <Toggle color="green" id="OverwriteFiles" name="OverwriteFiles">
        <Translate text="Overwrite Files (not recommended)" />
        <button type="button" class="btn-text-link ml-2" id="overwrite-files-info">
            <InfoCircleSolid />
        </button>
        <Tooltip class="max-w-md" triggeredBy="#overwrite-files-info">
            {overwriteFilesTooltip}
        </Tooltip>
    </Toggle>
    <Toggle color="green" id="DetectOtherLinks" name="DetectOtherLinks">
        <Translate text="Detect Other URL(s) like MEGA" />
        <button type="button" class="btn-text-link ml-2" id="detect-other-links-info">
            <InfoCircleSolid />
        </button>
        <Tooltip class="max-w-md" triggeredBy="#detect-other-links-info">
            {detectOtherLinksTooltip}
        </Tooltip>
    </Toggle>
    <Toggle color="green" id="UseCacheDb" name="UseCacheDb">
        <Translate text="Use Cache Database" />
        <button type="button" class="btn-text-link ml-2" id="use-cache-db-info">
            <InfoCircleSolid />
        </button>
        <Tooltip class="max-w-md" triggeredBy="#use-cache-db-info">
            {useCacheDbTooltip}
        </Tooltip>
    </Toggle>
</form>

{#if UseCacheDbInp} 
    <CacheDetails bind:open={cacheDetailsOpened} />
    <div class="mt-5">
        <button type="button" class="btn btn-info flex" on:click={() => cacheDetailsOpened = true} >
            <div class="text-main">
                <ArchiveSolid />
            </div>
            <Translate text="View Cache" />
        </button>
    </div>
{/if}
