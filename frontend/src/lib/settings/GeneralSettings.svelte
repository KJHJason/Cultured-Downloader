<script lang="ts">
    import { Toggle } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { GetPreferences, SetFantiaPreferences, SetGeneralPreferences } from "../../scripts/wailsjs/go/app/App";
    import { generalFormId, swal } from "../../scripts/constants";
    import { translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";
    import CacheDetails from "./CacheDetails.svelte";

    export let formId = generalFormId;
    export let promptSuccess: boolean;
    export let preferences: any = undefined;

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

    const processPrefs = (preferences: any) => {
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
            const prefs: Record<string, boolean> = {
                DlPostThumbnail:    DlPostThumbnailInp.checked,
                DlPostImages:       DlPostImagesInp.checked,
                DlPostAttachments:  DlPostAttachmentsInp.checked,
                OverwriteFiles:     OverwriteFilesInp.checked,
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
        </Toggle>
    {/if}
    {#if showDlGDriveInp}
        <Toggle color="green" id="DlGDrive" name="DlGDrive">
            <Translate text="Download GDrive Links" />
        </Toggle>
    {/if}
    <Toggle color="green" id="OverwriteFiles" name="OverwriteFiles">
        <Translate text="Overwrite Files (not recommended)" />
    </Toggle>
    <Toggle color="green" id="DetectOtherLinks" name="DetectOtherLinks">
        <Translate text="Detect Other URL(s) like MEGA" />
    </Toggle>
    <Toggle color="green" id="UseCacheDb" name="UseCacheDb">
        <Translate text="Use Cache Database" />
    </Toggle>
</form>

{#if UseCacheDbInp} 
    <CacheDetails bind:open={cacheDetailsOpened} />
    <div class="mt-5 text-right">
        <button type="button" class="btn btn-info" on:click={() => cacheDetailsOpened = true} >
            <Translate text="View Cache" />
        </button>
    </div>
{/if}
