<script lang="ts">
    import type { Writable } from "svelte/store";
    import CacheBase from "./CacheBase.svelte";
    import { GetAllKemonoCreatorCache, DeleteAllKemonoCreatorCache } from "../../../scripts/wailsjs/go/app/App";

    interface Props {
        rowsPerPage: number;
        pageNum: Writable<number>;
    }

    let { rowsPerPage, pageNum }: Props = $props();
    const parseValue = (arg: string) => arg;
</script>

<CacheBase
    {rowsPerPage}
    pageNum={pageNum}
    {parseValue}
    showKey={false}
    hasDateTime={false}
    valueTitle="Creator Name"
    deleteInProgTitle="Deleting Creator Name Cache..."
    deleteSuccessTitle="Creator Name Cache Cleared!"
    deleteSuccessText="Creator Name Cache has been cleared!"
    deleteAllCacheFunc={DeleteAllKemonoCreatorCache}
    deleteAllCacheText="Delete All Creator Name Cache"
    fetchDataFunc={GetAllKemonoCreatorCache}
/>
