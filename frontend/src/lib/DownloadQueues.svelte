<script lang="ts">
    import { Progressbar, Tooltip, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../scripts/wailsjs/runtime/runtime";
    import loadingImg from "../assets/images/bocchi-loading.gif";
    import { onMount } from "svelte";
    import { GetDownloadQueues } from "../scripts/wailsjs/go/app/App";
    import { FolderSolid, NewspaperSolid, StopSolid, TrashBinSolid } from "flowbite-svelte-icons";

    let downloadQueues: any[] = [];
    onMount(async () => {
        // make a polling request to get the download queues
        setInterval(async () => {
            const retrievedQueues = await GetDownloadQueues();
            downloadQueues = [...retrievedQueues];
        }, 400);
    });
</script>

<div class="container mx-auto">
    <h2 class="mb-3">Download Queues</h2>
    <Table hoverable={true} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>Thumbnail</TableHeadCell>
            <TableHeadCell>Title</TableHeadCell>
            <TableHeadCell>Progress</TableHeadCell>
            <TableHeadCell>Actions</TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#each downloadQueues as dlQ}
                <TableBodyRow>
                    <TableBodyCell>
                        {#if dlQ.ProgressBar.ThumbnailUrl === ""}
                            <!-- reassign thumbnail to loadingImg -->
                            <img class="object-cover h-auto w-14 rounded" src={loadingImg} alt="post-thumbnail">
                        {:else}
                            <img class="object-cover h-auto w-14 rounded" src={dlQ.ProgressBar.ThumbnailUrl} alt="post-thumbnail">
                        {/if}
                    </TableBodyCell>
                    <TableBodyCell class="whitespace-normal">
                        <button on:click={() => BrowserOpenURL(dlQ.ProgressBar.MainUrl)} class="btn-link break-words max-w-48 text-left">{dlQ.ProgressBar.Title}</button>
                    </TableBodyCell>
                    <TableBodyCell>
                        <div class="flex justify-between mb-1">
                            <span class="font-medium text-blue-700 dark:text-white">{dlQ.ProgressBar.Msg}</span>
                            <span class="text-sm font-medium text-blue-700 dark:text-white">{dlQ.ProgressBar.Percentage}%</span>
                        </div>
                        <Progressbar progress="{dlQ.ProgressBar.Percentage}" color="blue" animate={true} />
                    </TableBodyCell>
                    <TableBodyCell tdClass="max-w-40">
                        <!-- TODO: add download speed and eta info for each item to be downloaded on a modal -->
                        {#if !dlQ.ProgressBar.Finished}
                            <button id="view-{dlQ.Id}" on:click={() => BrowserOpenURL(dlQ.ProgressBar.FolderPath)} class="view btn btn-success">
                                <FolderSolid />
                            </button>
                            <Tooltip triggeredBy="#view-{dlQ.Id}">View Downloaded Files</Tooltip>
                        {:else}
                            <button class="btn btn-info" id="details-{dlQ.Id}">
                                <NewspaperSolid />
                            </button>
                            <button class="btn btn-danger" id="stop-{dlQ.Id}">
                                <StopSolid />
                            </button>
                            <button class="btn btn-danger" id="remove-{dlQ.Id}">
                                <TrashBinSolid />
                            </button>
                            <Tooltip triggeredBy="#details-{dlQ.Id}">View Download Details</Tooltip>
                            <Tooltip triggeredBy="#stop-{dlQ.Id}">Stop Download</Tooltip>
                            <Tooltip triggeredBy="#remove-{dlQ.Id}">Remove from Queue</Tooltip>
                        {/if}
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</div>
