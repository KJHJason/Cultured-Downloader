<script lang="ts">
    import { Modal, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { ClipboardListSolid } from "flowbite-svelte-icons";
    import Translate from "../common/Translate.svelte";
    import { onMount } from "svelte";
    import { translateText } from "../../scripts/language";
    import type { app } from "../../scripts/wailsjs/go/models";

    interface Props {
        dlQ: app.FrontendDownloadQueue;
        inputModalsId: Record<number, boolean>;
    }

    let { dlQ, inputModalsId = $bindable() }: Props = $props();
    let inputModalTitle = $state("");
    onMount(async () => {
        inputModalTitle = await translateText("Your Inputs");
    });
</script>

<button class="btn btn-info" onclick={() => {inputModalsId[dlQ.Id] = true}}>
    <ClipboardListSolid />
</button>
<Modal bind:open={inputModalsId[dlQ.Id]} title={inputModalTitle} id="view-inputs-{dlQ.Id}" size="lg" autoclose>
    <Table hoverable={false} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>
                <Translate text="Input" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Parsed URL (*may be inaccurate)" />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#each dlQ.Inputs as input}
                <TableBodyRow>
                    <TableBodyCell>
                        {input.Input}
                    </TableBodyCell>
                    <TableBodyCell>
                        <button class="text-link" onclick={() => BrowserOpenURL(input.Url)}>
                            {input.Url}
                        </button>
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</Modal>