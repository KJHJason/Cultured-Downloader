<script lang="ts">
    import { Progressbar, Modal, Tooltip, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Spinner } from "flowbite-svelte";
    import { BrowserOpenURL } from "../scripts/wailsjs/runtime/runtime";
    import loadingImg from "../assets/images/bocchi-loading.gif";
    import { onMount } from "svelte";
    import { GetDownloadQueues } from "../scripts/wailsjs/go/app/App";
    import { FolderSolid, NewspaperSolid, StopSolid, TrashBinSolid } from "flowbite-svelte-icons";

    let modalsId: Record<number, boolean> = {};
    let downloadQueues: any[] = [];
    onMount(async () => {
        // make a polling request to get the download queues
        setInterval(async () => {
            const retrievedQueues = await GetDownloadQueues();

            let activeId: number = -1;
            const newModalsId: Record<number, boolean> = {};
            for (const key in modalsId) {
                if (modalsId[key]) {
                    newModalsId[key] = true;
                    activeId = parseInt(key);
                    continue;
                }
            }
            for (const key in retrievedQueues) {
                const id = retrievedQueues[key].Id;
                if (activeId !== -1 && id === activeId) {
                    continue;
                }
                newModalsId[id] = false;
            }
            modalsId = newModalsId;

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
                        <button type="button" on:click={() => BrowserOpenURL(dlQ.ProgressBar.MainUrl)} class="btn-text-link break-words max-w-48 text-left">{dlQ.ProgressBar.Title}</button>
                    </TableBodyCell>
                    <TableBodyCell>
                        {@const success = dlQ.ProgressBar.Finished && !dlQ.ProgressBar.HasError}
                        {@const hasError = dlQ.ProgressBar.Finished && dlQ.ProgressBar.HasError}
                        <div class="flex justify-between mb-1">
                            {#if success}
                                <span class="pr-2 font-medium text-green-700 dark:text-white">{dlQ.SuccessMsg}</span>
                            {:else if hasError}
                                <span class="pr-2 font-medium text-red-700 dark:text-white">{dlQ.ErrMsg}</span>
                            {:else}
                                <span class="pr-2 font-medium text-blue-700 dark:text-white">{dlQ.Msg}</span>
                            {/if}
                            <span class="text-sm font-medium text-blue-700 dark:text-white">{dlQ.ProgressBar.Percentage}%</span>
                        </div>
                        {#if success}
                            <Progressbar progress="100" color="green" animate={true} />
                        {:else if hasError}
                            <Progressbar progress="100" color="red" animate={true} />
                        {:else}
                            <Progressbar progress="{dlQ.ProgressBar.Percentage}" color="blue" animate={true} />
                        {/if}
                    </TableBodyCell>
                    <TableBodyCell tdClass="text-center">
                        <!-- TODO: add download speed and eta info for each item to be downloaded on a modal -->
                        <!-- TODO: remove the ! in the condition check after testing -->
                        {#if !dlQ.ProgressBar.Finished}
                            <button type="button" id="view-{dlQ.Id}" on:click={() => BrowserOpenURL(dlQ.ProgressBar.FolderPath)} class="view btn btn-success">
                                <FolderSolid />
                            </button>
                            <Tooltip triggeredBy="#view-{dlQ.Id}">View Downloaded Files</Tooltip>
                        {:else}
                            <button type="button" class="btn-text-info" id="details-{dlQ.Id}" on:click={() => {modalsId[dlQ.Id] = true}}>
                                <NewspaperSolid />
                            </button>
                            <button type="button" class="btn-text-danger" id="stop-{dlQ.Id}">
                                <StopSolid />
                            </button>
                            <button type="button" class="btn-text-danger" id="remove-{dlQ.Id}">
                                <TrashBinSolid />
                            </button>
                            <Tooltip triggeredBy="#details-{dlQ.Id}">View Download Details</Tooltip>
                            <Tooltip triggeredBy="#stop-{dlQ.Id}">Stop Download</Tooltip>
                            <Tooltip triggeredBy="#remove-{dlQ.Id}">Remove from Queue</Tooltip>
                            <Modal bind:open={modalsId[dlQ.Id]} title="Download Details" id="view-details-{dlQ.Id}" size="lg" autoclose>
                                <Table hoverable={false} shadow={true}>
                                    <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
                                        <TableHeadCell>Filename</TableHeadCell>
                                        <TableHeadCell>Download Speed</TableHeadCell>
                                        <TableHeadCell>Progress/ETA</TableHeadCell>
                                    </TableHead>
                                    <TableBody tableBodyClass="divide-y">
                                        {#each dlQ.DlProgressBars as dlDetails}
                                            <TableBodyRow>
                                                <TableBodyCell>
                                                    <span class="break-words">
                                                        {#if dlDetails.Filename == ""}
                                                            Loading...
                                                        {:else}
                                                            {dlDetails.Filename}
                                                        {/if}
                                                    </span>
                                                </TableBodyCell>
                                                <TableBodyCell>
                                                    <span>{parseFloat(dlDetails.DownloadSpeed).toFixed(2)}</span>
                                                </TableBodyCell>
                                                <TableBodyCell>
                                                    {#if dlDetails.DownloadETA == -1}
                                                        <Spinner color="yellow" />
                                                        <span class="pl-2">Unknown ETA...</span>
                                                    {:else}
                                                        <div class="flex justify-between mb-1">
                                                            <span class="font-medium text-blue-700 dark:text-white pr-2">
                                                                {#if dlDetails.DownloadETA > 60}
                                                                    {(parseFloat(dlDetails.DownloadETA)/ 60).toFixed(2)} minutes
                                                                {:else if dlDetails.DownloadETA == 0}
                                                                    Downloaded!
                                                                {:else}
                                                                    {parseFloat(dlDetails.DownloadETA).toFixed(2)} seconds
                                                                {/if}
                                                            </span>
                                                            <span class="font-medium text-blue-700 dark:text-white">{dlDetails.Percentage}%</span>
                                                        </div>
                                                        <Progressbar progress="{dlDetails.Percentage}" color="blue" animate={true} />
                                                    {/if}
                                                </TableBodyCell>
                                            </TableBodyRow>
                                        {/each}
                                    </TableBody>
                                </Table>
                            </Modal>
                        {/if}
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</div>
