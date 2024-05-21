<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { Table, TableHead, TableHeadCell, TableBody, TableBodyCell, TableBodyRow, Search } from "flowbite-svelte";
    import Translate from "../../common/Translate.svelte";
    import Pagination from "../../common/Pagination.svelte";
    import { onMount } from "svelte";
    import { DeleteCacheKey } from "../../../scripts/wailsjs/go/app/App";
    import { makeDateTimeReadable } from "../../../scripts/utils/time";
    import { pleaseWaitSwal, swal } from "../../../scripts/constants";
    import { translateText } from "../../../scripts/language";
    import { TrashBinSolid } from "flowbite-svelte-icons";
    import type { app } from "../../../scripts/wailsjs/go/models";

    export let showKey: boolean = true;
    export let hasDateTime: boolean = true;
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
    export let fetchDataFunc: () => Promise<app.FrontendCacheKeyValue[]>;

    const cache: Writable<app.FrontendCacheKeyValue[]> = writable([]);
    const paginatedCache: Writable<app.FrontendCacheKeyValue[]> = writable([]);

    let translatedDeleteInProgTitle = "";
    let translatedDeleteInProgText = "";
    let translatedDeleteSuccessTitle = "";
    let translatedDeleteSuccessText = "";
    onMount(async() => {
        translatedDeleteInProgTitle = await translateText(deleteInProgTitle);
        translatedDeleteInProgText = await translateText(deleteInProgText);
        translatedDeleteSuccessTitle = await translateText(deleteSuccessTitle);
        translatedDeleteSuccessText = await translateText(deleteSuccessText);
    });

    const deleteKey = async (bucket:string, key: string) => {
        await DeleteCacheKey(bucket, key);
        cache.update(c => c.filter(c => c.Key !== key));
    };
    const wrappedDeleteAllCacheFunc = async () => {
        if ($cache.length === 0) { 
            return;
        }

        pleaseWaitSwal.fire({
            title: translatedDeleteInProgTitle,
            text: translatedDeleteInProgText,
        });
        await deleteAllCacheFunc();
        swal.fire({
            icon: "success",
            title: translatedDeleteSuccessTitle,
            text: translatedDeleteSuccessText,
            timer: 2000,
        });
    };
    const deleteAllKeys = async () => {
        await wrappedDeleteAllCacheFunc();
        pageNum.set(1);
        cache.set([]);
    };

    let originalElements: app.FrontendCacheKeyValue[] = [];
    let searchInput: HTMLInputElement;
    const processSearchInput = () => {
        const searchValue = searchInput.value.toLowerCase();
        pageNum.set(1);
        if (searchValue === "") {
            cache.set(originalElements);
            return;
        }
        cache.set(originalElements.filter(post => post.Key.toLowerCase().includes(searchValue)));
    };
    onMount(async () => {
        const searchPlaceholder = await translateText("Search");
        searchInput = document.getElementById("searchInput") as HTMLInputElement;
        searchInput.placeholder = searchPlaceholder;
        searchInput.addEventListener("input", processSearchInput);
    })
    onMount(async () => {
        const data = await fetchDataFunc();
        if (data === null) {
            cache.set([]);
            originalElements = [];
        } else {
            cache.set(data);
            originalElements = data;
        }
    });
</script>

<Search size="md" id="searchInput" class="rounded-none rounded-l" />

<div class="my-3">
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            {#if showKey}
                <TableHeadCell>
                    <Translate text={keyTitle} />
                </TableHeadCell>
            {/if}
            <TableHeadCell>
                <Translate text={valueTitle} />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Actions" />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if $cache.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan="{showKey ? 3 : 2}">
                        <Translate text="Nothing here!" />
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
                            {#if hasDateTime}
                                {parseValue(cache.DateTime)}
                            {:else}
                                {parseValue(cache.Value)}
                            {/if}
                        </TableBodyCell>
                        <TableBodyCell>
                            <button class="btn-text-danger" on:click={() => deleteKey(cache.Bucket, cache.Key)}>
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
            <Translate text={deleteAllCacheText} />
        </button>
    </div>
{/if}
