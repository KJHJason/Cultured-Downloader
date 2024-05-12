<script lang="ts">
    import { Translate } from "../scripts/language";
    import type { Writable } from "svelte/store";

    export let language: Writable<string>;
</script>

<div class="h-screen flex justify-center items-center">
    <div class="text-center">
        <h1 class="text-4xl font-bold">{Translate("Welcome to Cultured Downloader!", $language)}</h1>
    </div>
</div>
