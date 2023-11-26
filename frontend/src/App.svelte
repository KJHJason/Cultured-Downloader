<script>
    import Navbar from "./components/Navbar.svelte";
    import Home from "./components/Home.svelte";
    import Fantia from "./components/Fantia.svelte";

    let action = "home";
    const actions = {
        Home:        "home",
        Fantia:      "fantia",
        Pixiv:       "pixiv",
        PixivFanbox: "pixivFanbox",
        Kemono:      "kemono",
        Downloads:   "downloads",
        Settings:    "settings",
    };
</script>

<Navbar bind:action={action} actions={actions} />

<div class="p-4 sm:ml-64">
    <div class="mt-14">
        {#if action === actions.Home}
            <Home/>
        {:else if action === actions.Fantia}
            <Fantia/>
        {:else}
            <p>Not implemented yet</p>
        {/if}
    </div>
</div>
