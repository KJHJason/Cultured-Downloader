<script lang="ts">
    import { Modal, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { ClipboardListSolid } from "flowbite-svelte-icons";
    import { Translate } from "../../scripts/language";

    export let dlQ: any;
    export let inputModalsId: Record<number, boolean>;
</script>

<button class="btn btn-info" on:click={() => {inputModalsId[dlQ.Id] = true}}>
    <ClipboardListSolid />
</button>
<Modal bind:open={inputModalsId[dlQ.Id]} title="Your Inputs" id="view-inputs-{dlQ.Id}" size="md" autoclose>
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>{Translate("Input")}</TableHeadCell>
            <TableHeadCell>{Translate("Parsed URL (*may be inaccurate)")}</TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            <TableBodyRow>
                {#each dlQ.Inputs as input}
                    <TableBodyCell>
                        {input.Input}
                    </TableBodyCell>
                    <TableBodyCell>
                        <button class="text-link" on:click={() => BrowserOpenURL(input.Url)}>
                            {input.Url}
                        </button>
                    </TableBodyCell>
                {/each}
            </TableBodyRow>
        </TableBody>
    </Table>
</Modal>