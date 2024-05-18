<script lang="ts">
    import { Table, TableHead, TableHeadCell, TableBody, Dropdown, Checkbox, TableBodyCell, TableBodyRow } from "flowbite-svelte";
    import Translate from "../../common/Translate.svelte";
    import { writable, type Writable } from "svelte/store";
    import { translateText } from "../../../scripts/language";
    import { onDestroy, onMount } from "svelte";
    import Pagination from "../../common/Pagination.svelte";
    import { DeleteAllPostCache, DeleteCacheKey, GetPostCache } from "../../../scripts/wailsjs/go/app/App";
    import { pleaseWaitSwal, swal } from "../../../scripts/constants";
    import { FilterOutline, TrashBinSolid } from "flowbite-svelte-icons";
    import { makeDateTimeReadable } from "../../../scripts/time";

    export let rowsPerPage: number;
    export let pageNum: Writable<number>;
    export let language: Writable<string>;

    interface Platform {
        name: string;
        checked: boolean;
    }
    const platforms: Writable<Platform[]> = writable([
        { name: "Fantia", checked: false },
        { name: "Pixiv", checked: false },
        { name: "Pixiv Fanbox", checked: false },
        { name: "Kemono", checked: false },
        { name: "All", checked: false }
    ]);

    let selectAll = true;
    const toggleAllFilter = (allEnabled: boolean) => {
        if (allEnabled) {
            platforms.update(plats => plats.map(platform => ({ ...platform, checked: false })));
            selectAll = false;
        } else {
            platforms.update(plats => plats.map(platform => ({ ...platform, checked: true })));
            selectAll = true;
        }
    }
    onMount(() => {
        toggleAllFilter(false);
    });

    const postCache: Writable<any[]> = writable([]);
    const paginatedPostCache: Writable<any[]> = writable([]);
    const deleteCacheKey = async (key: string) => {
        await DeleteCacheKey(key);
        postCache.update(c => c.filter(c => c.CacheKey !== key));
    };
    const deleteAllPostCache = async () => {
        if ($postCache.length === 0) {
            return;
        }

        pleaseWaitSwal.fire({
            title: await translateText("Deleting Post Cache...", $language),
            text: await translateText("This may take a while. Please wait!", $language),
        });
        await DeleteAllPostCache();
        pageNum.set(1);
        postCache.set([]);
        swal.fire({
            title: await translateText("Post Cache Cleared!", $language),
            text: await translateText("Post Cache has been cleared!", $language),
            icon: "success",
            timer: 2000,
        });
    };

    const modalDetails = writable("")
    const getSelectedPlatforms = (): string[] => {
        if (selectAll) {
            return ["Fantia", "Pixiv", "Pixiv Fanbox", "Kemono"];
        }
        return $platforms.filter(platform => platform.checked).map(platform => platform.name);
    };
    const platformsUnsubscribe = platforms.subscribe(async () => {
        const comma = await translateText("filter_comma", $language, ", ");
        const noResult = await translateText("filter_none", $language, " None"); 

        const selectedPlatforms = getSelectedPlatforms();
        const filter = {
            Fantia: selectedPlatforms.includes("Fantia"),
            Pixiv: selectedPlatforms.includes("Pixiv"),
            PixivFanbox: selectedPlatforms.includes("Pixiv Fanbox"),
            Kemono: selectedPlatforms.includes("Kemono")
        }
        postCache.set(await GetPostCache(filter));

        modalDetails.update(() => {
            if (selectedPlatforms.length === 0) {
                return noResult;
            }
            return selectedPlatforms.join(comma);
        });
    });
    onDestroy(() => {
        platformsUnsubscribe();
    });

    const togglePlatform = (index: string): void => {
        if (index === "All") {
            toggleAllFilter(selectAll);
            return;
        } 

        platforms.update(plats => {
            // Note: due to binding, the checked value will be updated before togglePlatform is called
            const isChecked = plats.find(platform => platform.name === index)?.checked as boolean;
            if (selectAll && !isChecked) { // make All index unchecked and the current index unchecked
                selectAll = false;
                return plats.map(platform => (platform.name === "All" || platform.name === index ? { ...platform, checked: false } : platform));
            }
            return plats.map(platform => (platform.name === index ? { ...platform, checked: isChecked } : platform));
        });
    };
</script>

<div class="flex">
    <div>
        <Translate text="showing cache_front" {language} fallback="Showing cache for " />
        <span>{$modalDetails}</span><Translate text="showing filter_back" {language} fallback="." />
    </div>
    <div class="ml-auto">
        <button type="button" class="btn btn-info flex">
            <FilterOutline />
            <Translate text="Filter" {language} />
        </button>
        <Dropdown class="overflow-y-auto px-3 pb-3 text-sm h-44 text-left">
            {#each $platforms as platform }
                <li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
                    <Checkbox bind:checked={platform.checked} on:change={() => togglePlatform(platform.name)}>
                        {platform.name}
                    </Checkbox>
                </li>
            {/each}
        </Dropdown>
    </div>
</div>

<div class="mb-3">
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>
                <Translate text="Platform" {language} />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="URL" {language} />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Date/Time" {language} />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Actions" {language} />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if $postCache.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan="4">
                        <Translate text="Nothing here!" {language} />
                    </TableBodyCell>
                </TableBodyRow>
            {:else}
                {#each $paginatedPostCache as post }
                    <TableBodyRow>
                        <TableBodyCell>
                            {post.Platform}
                        </TableBodyCell>
                        <TableBodyCell>
                            <div class="text-wrap">
                                {post.Url}
                            </div>
                        </TableBodyCell>
                        <TableBodyCell>
                            {makeDateTimeReadable(post.Datetime)}
                        </TableBodyCell>
                        <TableBodyCell>
                            <button class="btn-text-danger" on:click={() => deleteCacheKey(post.CacheKey)}>
                                <TrashBinSolid />
                            </button>
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            {/if}
        </TableBody>
    </Table>
</div>

<Pagination {pageNum} {rowsPerPage} elements={postCache} paginatedEl={paginatedPostCache} />
{#if $postCache.length > 0}
    <div class="mt-3 text-right">
        <button class="btn btn-danger" on:click={deleteAllPostCache}>
            <Translate text="Clear All Post Cache" {language} />
        </button>
    </div>
{/if}
