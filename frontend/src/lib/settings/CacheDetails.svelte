<script lang="ts">
    import { Modal, Tabs, TabItem } from "flowbite-svelte";
    import { writable } from "svelte/store";
    import { ArchiveSolid, InfoCircleSolid } from "flowbite-svelte-icons";
    import PostCacheDetails from "./cache/PostCacheDetails.svelte";
    import { onMount } from "svelte";
    import { translateText } from "../../scripts/language";
    import GDriveCache from "./cache/GDriveCache.svelte";
    import KemonoCreatorsCache from "./cache/KemonoCreatorsCache.svelte";
    import UgoiraCache from "./cache/UgoiraCache.svelte";
    import Translate from "../common/Translate.svelte";

    let open: boolean;

    $: modalTitle = "";
    $: postCacheTitle = "Post Cache";
    $: gdriveCacheTitle = "GDrive Cache";
    $: kemonoCacheTitle = "Kemono Creator Cache";
    $: ugoiraCacheTitle = "Pixiv Ugoira Cache";
    onMount(async () => {
        modalTitle = await translateText("Cache Details");
        postCacheTitle = await translateText("Post Cache");
        gdriveCacheTitle = await translateText("GDrive Cache");
        kemonoCacheTitle = await translateText("Kemono Creator Cache");
        ugoiraCacheTitle = await translateText("Pixiv Ugoira Cache");
    });

    const rowsPerPage = 6;
    const postCachePageNum = writable(1);
    const gdriveCachePageNum = writable(1);
    const kemonoCachePageNum = writable(1);
    const ugoiraCachePageNum = writable(1);
</script>

<Modal bind:open={open} title="{modalTitle}" id="view-cache-details" size="lg" autoclose={false}>
    <Tabs tabStyle="underline">
        <TabItem open title={postCacheTitle}>
            <PostCacheDetails {rowsPerPage} pageNum={postCachePageNum} />
        </TabItem>
        <TabItem title={gdriveCacheTitle}>
            <GDriveCache {rowsPerPage} pageNum={gdriveCachePageNum} />
        </TabItem>
        <TabItem title={ugoiraCacheTitle}>
            <UgoiraCache {rowsPerPage} pageNum={ugoiraCachePageNum} />
        </TabItem>
        <TabItem title={kemonoCacheTitle}>
            <KemonoCreatorsCache {rowsPerPage} pageNum={kemonoCachePageNum} />
        </TabItem>
    </Tabs>
</Modal>

<div class="mt-5">
    <button type="button" class="btn btn-info flex" on:click={() => open = true} >
        <div class="text-main">
            <ArchiveSolid />
        </div>
        <Translate text="View Cache" />
    </button>
</div>
