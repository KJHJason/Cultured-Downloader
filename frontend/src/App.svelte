<script lang="ts">
    import "./scripts/dark-mode";
    import { actions, changeActionEventType } from "./scripts/constants";
    import Navbar from "./lib/Navbar.svelte";
    import Home from "./lib/Home.svelte";
    import Fantia from "./lib/Fantia.svelte";
    import Pixiv from "./lib/Pixiv.svelte";
    import PixivFanbox from "./lib/PixivFanbox.svelte";
    import Kemono from "./lib/Kemono.svelte";
    import DownloadQueues from "./lib/DownloadQueues.svelte";
    import Settings from "./lib/Settings.svelte";

    let action: string = "home";
    const handleActionChange = (event: CustomEvent<string>) => {
        switch (event.type) {
            case changeActionEventType:
                action = event.detail;
                break;
            default:
                throw new Error(`Unknown event type: ${event.type}`);
        }
    };
</script>

<Navbar action={action} on:changeAction={handleActionChange}/>

<main class="p-4">
    <div class="mt-14">
        {#if action === actions.Home}
            <Home/>
        {:else if action === actions.Fantia}
            <Fantia/>
        {:else if action === actions.Pixiv}
            <Pixiv/>
        {:else if action === actions.PixivFanbox}
            <PixivFanbox/>
        {:else if action === actions.Kemono}
            <Kemono/>
        {:else if action === actions.Downloads}
            <DownloadQueues/>
        {:else if action == actions.Settings}
            <Settings />
        {:else}
            <p>Not implemented yet</p>
        {/if}
    </div>
</main>
