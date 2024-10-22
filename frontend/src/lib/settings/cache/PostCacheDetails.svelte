<script lang="ts">
    import { Table, TableHead, TableHeadCell, TableBody, Dropdown, Checkbox, TableBodyCell, TableBodyRow, Search } from "flowbite-svelte";
    import Translate from "../../common/Translate.svelte";
    import { writable, type Writable } from "svelte/store";
    import { translateText } from "../../../scripts/language";
    import { onDestroy, onMount } from "svelte";
    import Pagination from "../../common/Pagination.svelte";
    import { DeleteAllPostCache, DeleteCacheKey, GetPostCache } from "../../../scripts/wailsjs/go/app/App";
    import { pleaseWaitSwal, swal } from "../../../scripts/constants";
    import { FilterOutline, TrashBinSolid } from "flowbite-svelte-icons";
    import { makeDateTimeReadable } from "../../../scripts/utils/time";
    import fantiaLogo from "../../../assets/images/logos/fantia-logo.png";
    import pixivFanboxLogo from "../../../assets/images/logos/pixiv-fanbox-logo.png";
    import pixivLogo from "../../../assets/images/logos/pixiv-logo.png";
    import kemonoLogo from "../../../assets/images/logos/kemono-logo.png";
    import type { database } from "../../../scripts/wailsjs/go/models";

    interface Props {
        rowsPerPage: number;
        pageNum: Writable<number>;
    }

    let { rowsPerPage, pageNum }: Props = $props();

    interface Platform {
        name: string;
        checked: boolean;
    }
    let translatedAll: string;
    const platforms: Writable<Platform[]> = writable([
        { name: "Fantia", checked: false },
        { name: "Pixiv", checked: false },
        { name: "Pixiv Fanbox", checked: false },
        { name: "Kemono", checked: false },
        { name: "All", checked: false }
    ]);
    onMount(async () => {
        translatedAll = await translateText("All");
        platforms.update(plats => plats.map(platform => ({ ...platform, name: platform.name === "All" ? translatedAll : platform.name })));
    });

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

    let translatedDeleteInProgTitle = "";
    let translatedDeleteInProgText = "";
    let translatedDeleteSuccessTitle = "";
    let translatedDeleteSuccessText = "";
    onMount(async () => {
        translatedDeleteInProgTitle = await translateText("Deleting Post Cache...");
        translatedDeleteInProgText = await translateText("This may take a while. Please wait!");
        translatedDeleteSuccessTitle = await translateText("Post Cache Cleared!");
        translatedDeleteSuccessText = await translateText("Post Cache has been cleared!");
    });

    const postCache: Writable<database.PostCache[]> = writable([]);
    const paginatedPostCache: Writable<database.PostCache[]> = writable([]);
    const deleteCacheKey = async (bucket: string, key: string) => {
        await DeleteCacheKey(bucket, key);
        postCache.update(c => c.filter(c => c.CacheKey !== key));
    };
    const deleteAllPostCache = async () => {
        if ($postCache.length === 0) {
            return;
        }

        pleaseWaitSwal.fire({
            title: translatedDeleteInProgTitle,
            text: translatedDeleteInProgText,
        });
        await DeleteAllPostCache();
        pageNum.set(1);
        postCache.set([]);
        swal.fire({
            title: translatedDeleteSuccessTitle,
            text: translatedDeleteSuccessText,
            icon: "success",
            timer: 2000,
        });
    };

    let originalElements: database.PostCache[] = [];
    let searchInput: HTMLInputElement;
    const processSearchInput = () => {
        const searchValue = searchInput.value.toLowerCase();
        pageNum.set(1);
        if (searchValue === "") {
            postCache.set(originalElements);
            return;
        }
        postCache.set(originalElements.filter(post => post.Url.toLowerCase().includes(searchValue)));
    };
    onMount(async () => {
        const searchPlaceholder = await translateText("Search");
        searchInput = document.getElementById("searchInput") as HTMLInputElement;
        searchInput.placeholder = searchPlaceholder;
        searchInput.addEventListener("input", processSearchInput);
    })

    const modalDetails = writable("")
    const getSelectedPlatforms = (): string[] => {
        if (selectAll) {
            return ["Fantia", "Pixiv", "Pixiv Fanbox", "Kemono"];
        }
        return $platforms.filter(platform => platform.checked).map(platform => platform.name);
    };
    const platformsUnsubscribe = platforms.subscribe(async () => {
        const comma = await translateText("filter_comma", "", ", ");
        const noResult = await translateText("filter_none", "", " None"); 

        const selectedPlatforms = getSelectedPlatforms();
        const filter = {
            Fantia: selectedPlatforms.includes("Fantia"),
            Pixiv: selectedPlatforms.includes("Pixiv"),
            PixivFanbox: selectedPlatforms.includes("Pixiv Fanbox"),
            Kemono: selectedPlatforms.includes("Kemono")
        }

        const data = await GetPostCache(filter);
        if (data === null) {
            postCache.set([]);
            originalElements = [];
        } else {
            postCache.set(data);
            originalElements = data;
        }
        pageNum.set(1);

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
        if (index === translatedAll) {
            toggleAllFilter(selectAll);
            return;
        } 

        platforms.update(plats => {
            // Note: due to binding, the checked value will be updated before togglePlatform is called
            const isChecked = plats.find(platform => platform.name === index)?.checked as boolean;
            if (selectAll && !isChecked) { // make All index unchecked and the current index unchecked
                selectAll = false;
                return plats.map(platform => (platform.name === translatedAll || platform.name === index ? { ...platform, checked: false } : platform));
            }
            return plats.map(platform => (platform.name === index ? { ...platform, checked: isChecked } : platform));
        });
    };
</script>

<div class="grid grid-cols-1 gap-y-3">
    <div>
        <Translate text="showing cache_front" fallback="Showing cache for " />
        <span>{$modalDetails}</span><Translate text="showing cache_back" fallback="." />
    </div>
    <div class="flex">
        <Search size="md" id="searchInput" class="rounded-none rounded-l" />
        <button type="button" class="btn btn-info flex whitespace-nowrap !rounded-l-none">
            <FilterOutline />
            <Translate text="Filter" />
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

<div class="my-3">
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>
                <Translate text="Platform" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="URL" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Date/Time" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Actions" />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if $postCache.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan={4}>
                        <Translate text="Nothing here!" />
                    </TableBodyCell>
                </TableBodyRow>
            {:else}
                {#each $paginatedPostCache as post }
                    <TableBodyRow>
                        <TableBodyCell>
                            {@const platform = post.Platform}
                            {#if platform === "fantia"}
                                <img src={fantiaLogo} class="w-8 h-8 me-2" alt="fantia logo" />
                            {:else if platform === "pixiv"}
                                <img src={pixivLogo} class="w-8 h-8 me-2" alt="pixiv logo" />
                            {:else if platform === "fanbox"}
                                <img src={pixivFanboxLogo} class="w-8 h-8 me-2" alt="pixiv fanbox logo" />
                            {:else if platform === "kemono"}
                                <img src={kemonoLogo} class="w-8 h-8 me-2" alt="kemono logo" />
                            {:else}
                                {platform}
                            {/if}
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
                            <button class="btn-text-danger" onclick={() => deleteCacheKey(post.Bucket, post.CacheKey)}>
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
        <button class="btn btn-danger" onclick={deleteAllPostCache}>
            <Translate text="Clear All Post Cache" />
        </button>
    </div>
{/if}
