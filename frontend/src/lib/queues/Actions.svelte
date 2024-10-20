<script lang="ts">
    import { Modal, Tooltip, Table, TableBody, TableHead, TableHeadCell, TableBodyRow, TableBodyCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import {  GetFrontendDownloadDetails } from "../../scripts/wailsjs/go/app/App";
    import { ClipboardListSolid, FolderSolid, NewspaperSolid, StopSolid, TrashBinSolid } from "flowbite-svelte-icons";
    import { translateText } from "../../scripts/language";
    import DownloadDetails from "./DownloadDetails.svelte";
    import Errors from "./Errors.svelte";
    import { CancelQueue, DeleteQueue } from "../../scripts/wailsjs/go/app/App";
    import Pagination from "../common/Pagination.svelte";
    import { writable, type Writable } from "svelte/store";
    import { type dlModals } from "../../scripts/download";
    import { onDestroy, onMount } from "svelte";
    import Translate from "../common/Translate.svelte";
    import type { app } from "../../scripts/wailsjs/go/models";

    export let dlQ: app.FrontendDownloadQueue;
    export let modalsId: Record<number, dlModals>;
    export let errModalsId: Record<number, boolean>;

    let getDlDetailsInterval: number;
    const elements: Writable<app.FrontendDownloadDetails[]> = writable([]);
    let pageNum = writable(modalsId[dlQ.Id].pageNum);
    const pageNumEditUnsubscribe = pageNum.subscribe((val) => modalsId[dlQ.Id].pageNum = val);

    $: viewDownloadDetails = "";
    $: viewDownloadFiles = "";
    $: viewErrors = "";
    $: stopDownload = "";
    $: removeFromQueue = "";
    $: downloadDetailsModalTitle = "";

    onMount(async () => {
        getDlDetailsInterval = setInterval(async () => {
            if (!modalsId[dlQ.Id].open) {
                return;
            }

            const dlDetails = await GetFrontendDownloadDetails(dlQ.Id);
            elements.set(dlDetails);
        }, 1000);

        viewDownloadDetails = await translateText("View Download Details");
        viewDownloadFiles = await translateText("View Downloaded Files");
        viewErrors = await translateText("View Errors");
        stopDownload = await translateText("Stop Download");
        removeFromQueue = await translateText("Remove from Queue");
        downloadDetailsModalTitle = await translateText("Download Details");
    });

    onDestroy(() => {
        clearInterval(getDlDetailsInterval);
        pageNumEditUnsubscribe()
    });

    const rowsPerPage = 8;
    const paginatedDownloads: Writable<app.FrontendDownloadDetails[]> = writable([]);
</script>

<button type="button" class="btn-text-info" id="details-{dlQ.Id}" on:click={() => {modalsId[dlQ.Id].open = true}}>
    <NewspaperSolid />
</button>
<Tooltip triggeredBy="#details-{dlQ.Id}">{viewDownloadDetails}</Tooltip>

<Modal bind:open={modalsId[dlQ.Id].open} title={downloadDetailsModalTitle} id="view-details-{dlQ.Id}" size="lg" autoclose={false}>
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>
                <Translate text="Filename" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="File Size" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Download Speed" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Progress/ETA" />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if $paginatedDownloads.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan={4}>
                        <Translate text="Nothing here!" />
                    </TableBodyCell>
                </TableBodyRow>
            {:else}
                {#each $paginatedDownloads as dlDetails}
                    <DownloadDetails {dlDetails} />
                {/each}
            {/if}
        </TableBody>
    </Table>
    <Pagination {rowsPerPage} {pageNum} {elements} paginatedEl={paginatedDownloads} />
</Modal>

{#if dlQ.Finished}
    {#if !dlQ.HasError}
        <button type="button" id="view-{dlQ.Id}" on:click={() => BrowserOpenURL(dlQ.ProgressBar.FolderPath)} class="view btn-text-success">
            <FolderSolid />
        </button>
        <Tooltip triggeredBy="#view-{dlQ.Id}">{viewDownloadFiles}</Tooltip>
    {:else}
        <button type="button" class="btn-text-danger" id="errors-{dlQ.Id}" on:click={() => {errModalsId[dlQ.Id] = true}}>
            <ClipboardListSolid />
        </button>
        <Tooltip triggeredBy="#errors-{dlQ.Id}">{viewErrors}</Tooltip>

        <Modal bind:open={errModalsId[dlQ.Id]} title="Errors Logs" id="view-errors-{dlQ.Id}" size="lg" autoclose>
            <Errors errors={dlQ.ErrSlice} />
        </Modal>
    {/if}
{:else}
    <button type="button" class="btn-text-danger" id="stop-{dlQ.Id}" on:click={() => CancelQueue(dlQ.Id)}>
        <StopSolid />
    </button>
    <Tooltip triggeredBy="#stop-{dlQ.Id}">{stopDownload}</Tooltip>
{/if}

<button type="button" class="btn-text-danger" id="remove-{dlQ.Id}" on:click={() => DeleteQueue(dlQ.Id)}>
    <TrashBinSolid />
</button>
<Tooltip triggeredBy="#remove-{dlQ.Id}">{removeFromQueue}</Tooltip>
