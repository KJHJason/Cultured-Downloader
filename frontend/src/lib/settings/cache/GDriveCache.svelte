<script lang="ts">
    import type { Writable } from "svelte/store";
    import CacheBase from "./CacheBase.svelte";
    import { GetAllGdriveCache, DeleteAllGdriveCache } from "../../../scripts/wailsjs/go/app/App";

    interface Props {
        rowsPerPage: number;
        pageNum: Writable<number>;
    }

    let { rowsPerPage, pageNum }: Props = $props();
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
