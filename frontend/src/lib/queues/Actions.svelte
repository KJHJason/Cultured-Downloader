<script lang="ts">
    import { Modal, Tooltip, Table, TableBody, TableHead, TableHeadCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { FolderSolid, NewspaperSolid, StopSolid, TrashBinSolid } from "flowbite-svelte-icons";
    import { Translate } from "../../scripts/language";
    import DownloadDetails from "./DownloadDetails.svelte";

    export let dlQ: any;
    export let modalsId: Record<number, boolean>;
</script>

{#if dlQ.Finished}
    <button type="button" id="view-{dlQ.Id}" on:click={() => BrowserOpenURL(dlQ.ProgressBar.FolderPath)} class="view btn btn-success">
        <FolderSolid />
    </button>
    <Tooltip triggeredBy="#view-{dlQ.Id}">{Translate("View Downloaded Files")}</Tooltip>
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
    <Tooltip triggeredBy="#details-{dlQ.Id}">{Translate("View Download Details")}</Tooltip>
    <Tooltip triggeredBy="#stop-{dlQ.Id}">{Translate("Stop Download")}</Tooltip>
    <Tooltip triggeredBy="#remove-{dlQ.Id}">{Translate("Remove from Queue")}</Tooltip>

    <Modal bind:open={modalsId[dlQ.Id]} title="Download Details" id="view-details-{dlQ.Id}" size="lg" autoclose>
        <Table hoverable={false} shadow={true}>
            <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
                <TableHeadCell>{Translate("Filename")}</TableHeadCell>
                <TableHeadCell>{Translate("Download Speed")}</TableHeadCell>
                <TableHeadCell>{Translate("Progress/ETA")}</TableHeadCell>
            </TableHead>
            <TableBody tableBodyClass="divide-y">
                <DownloadDetails dlQ={dlQ} />
            </TableBody>
        </Table>
    </Modal>
{/if}