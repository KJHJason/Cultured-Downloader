<script lang="ts">
    import { Progressbar, Modal, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Spinner } from "flowbite-svelte";
    import { Translate } from "../../scripts/language";

    export let dlQ: any;
    export let progHistoryModalsId: Record<number, boolean>;
    export let makeDateTimeReadable: (dateTime: string, addSeconds: boolean) => string;

    const success = dlQ.Finished && !dlQ.HasError;
    const hasError = dlQ.Finished && dlQ.HasError;
</script>

<div class="flex items-center mb-1">
    {#if !success && !hasError && dlQ.ProgressBar.IsSpinner}
        <Spinner color="blue" />
    {/if}
    {#if success}
        <span class="px-2 font-medium">{dlQ.SuccessMsg}</span>
    {:else if hasError}
        <span class="px-2 font-medium">{dlQ.ErrMsg}</span>
    {:else}
        <span class="px-2 font-medium">{dlQ.Msg}</span>
    {/if}
</div>

{#if success}
    <Progressbar progress="100" color="green" animate={true} />
{:else if hasError}
    <Progressbar progress="100" color="red" animate={true} />
{:else}
    <Progressbar progress="{dlQ.ProgressBar.Percentage}" color="blue" animate={true} />
{/if}

{#if dlQ.NestedProgressBar?.length > 0}
    <div class="text-right mt-2">
        <button type="button" class="btn-text-info text-xs" id="view-prog-{dlQ.Id}" on:click={() => {progHistoryModalsId[dlQ.Id] = true}}>
            {Translate("View previous tasks...")}
        </button>
    </div>
    <Modal bind:open={progHistoryModalsId[dlQ.Id]} title="Tasks History" id="view-prog-{dlQ.Id}" size="md" autoclose>
        <Table hoverable={false} shadow={true}>
            <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
                <TableHeadCell>{Translate("Date/Time")}</TableHeadCell>
                <TableHeadCell>{Translate("Progress")}</TableHeadCell>
            </TableHead>
            <TableBody tableBodyClass="divide-y">
                {#if dlQ.NestedProgressBar.length === 0}
                    <TableBodyRow>
                        <TableBodyCell tdClass="text-center p-3" colspan="3">
                            {Translate("Nothing here!")}
                        </TableBodyCell>
                    </TableBodyRow>
                {:else}
                {#each dlQ.NestedProgressBar as nestedProgBar}
                    <TableBodyRow>
                        <TableBodyCell>
                            {makeDateTimeReadable(nestedProgBar.DateTime, true)}
                        </TableBodyCell>
                        <TableBodyCell>
                            <div class="flex justify-between mb-1">
                                {#if nestedProgBar.HasError}
                                    <span class="font-medium pr-2">{nestedProgBar.ErrMsg}</span>
                                {:else}
                                    <span class="font-medium pr-2">{nestedProgBar.SuccessMsg}</span>
                                {/if}
                            </div>

                            {#if nestedProgBar.HasError}
                                <Progressbar progress="{nestedProgBar.Percentage}" color="red" animate={true} />
                            {:else}
                                <Progressbar progress="100" color="green" animate={true} />
                            {/if}
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
                {/if}
            </TableBody>
        </Table>
    </Modal>
{/if}
