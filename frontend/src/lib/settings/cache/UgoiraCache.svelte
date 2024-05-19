<script lang="ts">
    import type { Writable } from "svelte/store";
    import CacheBase from "./CacheBase.svelte";
    import { GetAllUgoiraCache, DeleteAllUgoiraCache } from "../../../scripts/wailsjs/go/app/App";

    export let rowsPerPage: number;
    export let pageNum: Writable<number>;
</script>

<CacheBase
    {rowsPerPage}
    pageNum={pageNum}
    deleteInProgTitle="Deleting Ugoira Cache..."
    deleteSuccessTitle="Ugoira Cache Cleared!"
    deleteSuccessText="Ugoira Cache has been cleared!"
    deleteAllCacheFunc={DeleteAllUgoiraCache}
    deleteAllCacheText="Delete All Ugoira Cache"
    fetchDataFunc={GetAllUgoiraCache}
/>
