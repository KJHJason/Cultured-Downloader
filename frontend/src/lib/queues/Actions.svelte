<script lang="ts">
    import { Modal, Tooltip, Table, TableBody, TableHead, TableHeadCell, TableBodyRow, TableBodyCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { ClipboardListSolid, FolderSolid, NewspaperSolid, StopSolid, TrashBinSolid } from "flowbite-svelte-icons";
    import { Translate } from "../../scripts/language";
    import DownloadDetails from "./DownloadDetails.svelte";
    import Errors from "./Errors.svelte";
    import { CancelQueue, DeleteQueue } from "../../scripts/wailsjs/go/app/App";

    export let dlQ: any;
    export let modalsId: Record<number, boolean>;
    export let errModalsId: Record<number, boolean>;
</script>

<button type="button" class="btn-text-info" id="details-{dlQ.Id}" on:click={() => {modalsId[dlQ.Id] = true}}>
    <NewspaperSolid />
</button>
<Tooltip triggeredBy="#details-{dlQ.Id}">{Translate("View Download Details")}</Tooltip>

<Modal bind:open={modalsId[dlQ.Id]} title="Download Details" id="view-details-{dlQ.Id}" size="lg" autoclose>
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>{Translate("Filename")}</TableHeadCell>
            <TableHeadCell>{Translate("Download Speed")}</TableHeadCell>
            <TableHeadCell>{Translate("Progress/ETA")}</TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if dlQ.DlProgressBars.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan="3">
                        {Translate("Nothing here!")}
                    </TableBodyCell>
                </TableBodyRow>
            {:else}
                {#each dlQ.DlProgressBars as dlDetails}
                    <DownloadDetails {dlDetails} />
                {/each}
            {/if}
        </TableBody>
    </Table>
</Modal>

{#if dlQ.Finished}
    {#if !dlQ.HasError}
        <button type="button" id="view-{dlQ.Id}" on:click={() => BrowserOpenURL(dlQ.ProgressBar.FolderPath)} class="view btn-text-success">
            <FolderSolid />
        </button>
        <Tooltip triggeredBy="#view-{dlQ.Id}">{Translate("View Downloaded Files")}</Tooltip>
    {:else}
        <button type="button" class="btn-text-danger" id="errors-{dlQ.Id}" on:click={() => {errModalsId[dlQ.Id] = true}}>
            <ClipboardListSolid />
        </button>
        <Tooltip triggeredBy="#errors-{dlQ.Id}">{Translate("View Errors")}</Tooltip>

        <Modal bind:open={errModalsId[dlQ.Id]} title="Errors Logs" id="view-errors-{dlQ.Id}" size="lg" autoclose>
            <Errors errors={dlQ.ErrSlice} />
        </Modal>
    {/if}
{:else}
    <button type="button" class="btn-text-danger" id="stop-{dlQ.Id}" on:click={() => CancelQueue(dlQ.Id)}>
        <StopSolid />
    </button>
    <button type="button" class="btn-text-danger" id="remove-{dlQ.Id}" on:click={() => DeleteQueue(dlQ.Id)}>
        <TrashBinSolid />
    </button>
    <Tooltip triggeredBy="#stop-{dlQ.Id}">{Translate("Stop Download")}</Tooltip>
    <Tooltip triggeredBy="#remove-{dlQ.Id}">{Translate("Remove from Queue")}</Tooltip>
{/if}