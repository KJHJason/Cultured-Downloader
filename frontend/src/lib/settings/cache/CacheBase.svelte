<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { Table, TableHead, TableHeadCell, TableBody, TableBodyCell, TableBodyRow } from "flowbite-svelte";
    import Translate from "../../common/Translate.svelte";
    import Pagination from "../../common/Pagination.svelte";
    import { onMount } from "svelte";
    import { DeleteCacheKey } from "../../../scripts/wailsjs/go/app/App";
    import { makeDateTimeReadable } from "../../../scripts/time";
    import { pleaseWaitSwal, swal } from "../../../scripts/constants";
    import { translateText } from "../../../scripts/language";
    import { TrashBinSolid } from "flowbite-svelte-icons";

    export let showKey: boolean = true;
    export let keyTitle: string = "URL";
    export let valueTitle: string = "Date/Time";
    export let parseValue: (arg: string) => string = makeDateTimeReadable;
    export let deleteAllCacheText: string;
    export let deleteAllCacheFunc: () => Promise<void>;
    export let deleteInProgTitle: string;
    export let deleteInProgText: string = "This may take a while. Please wait!";
    export let deleteSuccessTitle: string;
    export let deleteSuccessText: string;

    export let rowsPerPage: number;
    export let pageNum: Writable<number>;
    export let language: Writable<string>;
    export let fetchDataFunc: () => Promise<any[]>;

    const cache: Writable<any[]> = writable([]);
    const paginatedCache: Writable<any[]> = writable([]);

    const deleteKey = async (key: string) => {
        await DeleteCacheKey(key);
        cache.update(c => c.filter(c => c.Key !== key));
    };
    const wrappedDeleteAllCacheFunc = async () => {
        if ($cache.length === 0) { 
            return;
        }

        pleaseWaitSwal.fire({
            title: await translateText(deleteInProgTitle, $language),
            text: await translateText(deleteInProgText, $language),
        });
        await deleteAllCacheFunc();
        swal.fire({
            title: await translateText(deleteSuccessTitle, $language),
            icon: "success",
            text: await translateText(deleteSuccessText, $language),
            timer: 2000,
        });
    };
    const deleteAllKeys = async () => {
        await wrappedDeleteAllCacheFunc();
        pageNum.set(1);
        cache.set([]);
    };

    onMount(async () => {
        console.log(await fetchDataFunc());
        cache.set(await fetchDataFunc());
    });
</script>

<div class="mb-3">
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            {#if showKey}
                <TableHeadCell>
                    <Translate text={keyTitle} {language} />
                </TableHeadCell>
            {/if}
            <TableHeadCell>
                <Translate text={valueTitle} {language} />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Actions" {language} />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if $cache.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan="{showKey ? 3 : 2}">
                        <Translate text="Nothing here!" {language} />
                    </TableBodyCell>
                </TableBodyRow>
            {:else}
                {#each $paginatedCache as cache }
                    <TableBodyRow>
                        {#if showKey}
                            <TableBodyCell>
                                <div class="text-wrap">
                                    {cache.Key}
                                </div>
                            </TableBodyCell>
                        {/if}
                        <TableBodyCell>
                            {parseValue(cache.Val)}
                        </TableBodyCell>
                        <TableBodyCell>
                            <button class="btn-text-danger" on:click={() => deleteKey(cache.CacheKey)}>
                                <TrashBinSolid />
                            </button>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            {/if}
        </TableBody>
    </Table>
</div>
<Pagination {pageNum} {rowsPerPage} elements={cache} paginatedEl={paginatedCache} />
{#if $cache.length > 0}
    <div class="mt-3 text-right">
        <button class="btn btn-danger" on:click={deleteAllKeys}>
            <Translate text={deleteAllCacheText} {language} />
        </button>
    </div>
{/if}
