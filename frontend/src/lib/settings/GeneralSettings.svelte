<script lang="ts">
    import { Toggle } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { GetPreferences, SetGeneralPreferences } from "../../scripts/wailsjs/go/app/App";
    import { generalFormId, swal } from "../../scripts/constants";

    export let formId = generalFormId;
    export let promptSuccess: boolean;
    export let preferences: any = undefined;

    onMount(async() => {
        const DlPostThumbnailInp = document.getElementById("DlPostThumbnail") as HTMLInputElement;
        const DlPostImagesInp = document.getElementById("DlPostImages") as HTMLInputElement;
        const DlPostAttachmentsInp = document.getElementById("DlPostAttachments") as HTMLInputElement;
        const DlGDriveInp = document.getElementById("DlGDrive") as HTMLInputElement;
        const OverwriteFilesInp = document.getElementById("OverwriteFiles") as HTMLInputElement;
        const DetectOtherLinksInp = document.getElementById("DetectOtherLinks") as HTMLInputElement;

        if (preferences === undefined) {
            preferences = await GetPreferences();
        }
        DlPostThumbnailInp.checked   = preferences.DlPostThumbnail;
        DlPostImagesInp.checked      = preferences.DlPostImages;
        DlPostAttachmentsInp.checked = preferences.DlPostAttachments;
        DlGDriveInp.checked          = preferences.DlGDrive;
        OverwriteFilesInp.checked    = preferences.OverwriteFiles;
        DetectOtherLinksInp.checked  = preferences.DetectOtherLinks;

        const prefForm = document.getElementById(formId) as HTMLFormElement;
        prefForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const prefs = {
                DlPostThumbnail:    DlPostThumbnailInp.checked,
                DlPostImages:       DlPostImagesInp.checked,
                DlPostAttachments:  DlPostAttachmentsInp.checked,
                DlGDrive:           DlGDriveInp.checked,
                OverwriteFiles:     OverwriteFilesInp.checked,
                DetectOtherLinks:   DetectOtherLinksInp.checked,
            };
            await SetGeneralPreferences(prefs);

            if (promptSuccess) {
                swal.fire({
                    title: "Success",
                    text: "Preferences saved successfully",
                    icon: "success",
                });
            }
        });
    });
</script>

<form id={formId} class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
    <Toggle color="green" id="DlPostThumbnail" name="DlPostThumbnail">Download Post Thumbnail</Toggle>
    <Toggle color="green" id="DlPostImages" name="DlPostImages">Download Post Images</Toggle>
    <Toggle color="green" id="DlPostAttachments" name="DlPostAttachments">Download Post Attachments</Toggle>
    <Toggle color="green" id="DlGDrive" name="DlGDrive">Download GDrive Links</Toggle>
    <Toggle color="green" id="OverwriteFiles" name="OverwriteFiles">Overwrite Files</Toggle>
    <Toggle color="green" id="DetectOtherLinks" name="DetectOtherLinks">Detect Other URL(s) like MEGA</Toggle>
</form>