<script lang="ts">
    import { Toggle } from "flowbite-svelte";
    import PixivSettings from "./PixivSettings.svelte";
</script>

<div class="grid grid-cols-1 gap-y-6">
    <div>
        <h4>General</h4>
        <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <Toggle color="green" name="DlPostThumbnail">Post Thumbnail</Toggle>
            <Toggle color="green" name="DlPostImages">Post Images</Toggle>
            <Toggle color="green" name="DlPostAttachments">Post Attachments</Toggle>
            <Toggle color="green" name="OverwriteFiles">Overwrite Files</Toggle>
            <Toggle color="green" name="DlGDrive">GDrive Links</Toggle>
            <Toggle color="green" name="DetectOtherLinks">Detect Other URL(s) like MEGA</Toggle>
        </div>
    </div>
    <div>
        <h4>Pixiv Specific</h4>
        <PixivSettings />
    </div>
</div>
<div class="text-right mt-4">
    <button class="btn btn-success">
        Save All
    </button>
</div>
