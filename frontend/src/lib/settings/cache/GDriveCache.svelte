<script lang="ts">
    import type { Writable } from "svelte/store";
    import CacheBase from "./CacheBase.svelte";
    import { GetAllGdriveCache, DeleteAllGdriveCache } from "../../../scripts/wailsjs/go/app/App";

    export let rowsPerPage: number;
    export let pageNum: Writable<number>;
</script>

<CacheBase
    {rowsPerPage}
    pageNum={pageNum}
    deleteInProgTitle="Deleting GDrive Cache..."
    deleteSuccessTitle="GDrive Cache Cleared!"
    deleteSuccessText="GDrive Cache has been cleared!"
    deleteAllCacheFunc={DeleteAllGdriveCache}
    deleteAllCacheText="Delete All GDrive Cache"
    fetchDataFunc={GetAllGdriveCache}
/>
