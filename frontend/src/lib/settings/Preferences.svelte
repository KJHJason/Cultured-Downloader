<script lang="ts">
    import { Hr, Spinner } from "flowbite-svelte";
    import PixivSettings from "./PixivSettings.svelte";
    import { GetPreferences } from "../../scripts/wailsjs/go/app/App";
    import GeneralSettings from "./GeneralSettings.svelte";
    import MergedSettings from "./MergedSettings.svelte";
    import Translate from "../common/Translate.svelte";
</script>

{#await GetPreferences()}
    <div class="flex">
        <Spinner color="blue" /> <p class="ms-3"><Translate text="Loading form..."/></p>
    </div>
{:then preferences}
    <h4>
        <Translate text="General" />
    </h4>
    <GeneralSettings promptSuccess={false} preferences={preferences} />
    <Hr />
    <h4>
        <Translate text="Pixiv Specific" />
    </h4>
    <PixivSettings promptSuccess={false} preferences={preferences} />
{/await}
<MergedSettings btnString="Save All" />
