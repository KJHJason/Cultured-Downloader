<script lang="ts">
    import { Spinner } from "flowbite-svelte";
    import PixivSettings from "./PixivSettings.svelte";
    import { GetPreferences } from "../../scripts/wailsjs/go/app/App";
    import GeneralSettings from "./GeneralSettings.svelte";
    import MergedSettings from "./MergedSettings.svelte";
</script>

<div class="grid grid-cols-1 gap-y-6">
    {#await GetPreferences()}
        <div class="flex">
            <Spinner color="blue" /> <p class="ms-3">Loading form...</p>
        </div>
    {:then preferences}
        <div>
            <h4>General</h4>
            <GeneralSettings promptSuccess={false} preferences={preferences} />
        </div>
        <div>
            <h4>Pixiv Specific</h4>
            <PixivSettings promptSuccess={false} preferences={preferences} />
        </div>
    {/await}
</div>
<MergedSettings btnString="Save All" />
