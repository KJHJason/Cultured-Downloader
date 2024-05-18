<script lang="ts">
    import { Modal, Tabs, TabItem } from "flowbite-svelte";
    import { type  Writable, writable } from "svelte/store";
    import PostCacheDetails from "./cache/PostCacheDetails.svelte";
    import Translate from "../common/Translate.svelte";
    import { onDestroy, onMount } from "svelte";
    import { translateText } from "../../scripts/language";
    import GDriveCache from "./cache/GDriveCache.svelte";
    import KemonoCreatorsCache from "./cache/KemonoCreatorsCache.svelte";
    import UgoiraCache from "./cache/UgoiraCache.svelte";

    export let open: boolean;
    export let language: Writable<string>;

    $: modalTitle = "";
    $: postCacheTitle = "Post Cache";
    $: gdriveCacheTitle = "GDrive Cache";
    $: kemonoCacheTitle = "Kemono Creator Cache";
    $: ugoiraCacheTitle = "Pixiv Ugoira Cache";
    const unsubscribeLanguage = language.subscribe(async lang => {
        postCacheTitle = await translateText("Post Cache", lang);
    });
    onDestroy(() => {
        unsubscribeLanguage();
    });
    onMount(async () => {
        modalTitle = await translateText("Cache Details", $language);
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
            <PostCacheDetails {language} {rowsPerPage} pageNum={postCachePageNum} />
        </TabItem>
        <TabItem title={gdriveCacheTitle}>
            <GDriveCache {language} {rowsPerPage} pageNum={gdriveCachePageNum} />
        </TabItem>
        <TabItem title={ugoiraCacheTitle}>
            <UgoiraCache {language} {rowsPerPage} pageNum={ugoiraCachePageNum} />
        </TabItem>
        <TabItem title={kemonoCacheTitle}>
            <KemonoCreatorsCache {language} {rowsPerPage} pageNum={kemonoCachePageNum} />
        </TabItem>
    </Tabs>
</Modal>
