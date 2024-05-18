<script lang="ts">
    import type { Writable } from "svelte/store";
    import CacheBase from "./CacheBase.svelte";
    import { GetAllKemonoCreatorCache, DeleteAllKemonoCreatorCache } from "../../../scripts/wailsjs/go/app/App";

    export let rowsPerPage: number;
    export let pageNum: Writable<number>;
    export let language: Writable<string>;
    const parseValue = (arg: string) => arg;
</script>

<CacheBase
    {language}
    {rowsPerPage}
    pageNum={pageNum}
    {parseValue}
    showKey={false}
    valueTitle="Creator Name"
    deleteInProgTitle="Deleting Creator Name Cache..."
    deleteSuccessTitle="Creator Name Cache Cleared!"
    deleteSuccessText="Creator Name Cache has been cleared!"
    deleteAllCacheFunc={DeleteAllKemonoCreatorCache}
    deleteAllCacheText="Delete All Creator Name Cache"
    fetchDataFunc={GetAllKemonoCreatorCache}
/>
