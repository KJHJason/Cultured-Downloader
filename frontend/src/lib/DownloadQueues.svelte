<script lang="ts">
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { onDestroy } from "svelte";
    import { GetDownloadQueues } from "../scripts/wailsjs/go/app/App";
    import { translate } from "../scripts/language";
    import { makeDateTimeReadable } from "../scripts/utils/time";
    import Inputs from "./queues/Inputs.svelte";
    import Tasks from "./queues/Tasks.svelte";
    import Actions from "./queues/Actions.svelte";
    import { actions } from "../scripts/constants";
    import type { Writable } from "svelte/store";
    import { type dlModals } from "../scripts/download";
    import Translate from "./common/Translate.svelte";
    import type { app } from "../scripts/wailsjs/go/models";

    interface Props {
        action: Writable<string>;
    }

    let { action }: Props = $props();

    let inputModalsId: Record<number, boolean> = {};
    let progHistoryModalsId: Record<number, boolean> = {}; 
    let modalsId: Record<number, dlModals> = {};
    let errModalsId: Record<number, boolean> = {};
    let downloadQueues: app.FrontendDownloadQueue[] = $state([]);

    type RecordType = Record<number, dlModals> | Record<number, boolean>;
    const modalLogic = <T extends RecordType>(oldRecord: T, queues: app.FrontendDownloadQueue[], defaultValue: () => dlModals | boolean): void => {
        let seen: Set<number> = new Set();
        for (const queue of queues) {
            const id = queue.Id;
            seen.add(id);

            if (oldRecord[id] === undefined) {
                oldRecord[id] = defaultValue();
            }
        }

        for (const key in oldRecord) {
            const id = parseInt(key);
            if (!seen.has(id)) {
                delete oldRecord[id];
            }
        }
    };

    // make a polling request to get the download queues
    let intervalId: number;    
    const unsubscribeAction = action.subscribe((curAction: string) => {
        if (curAction !== actions.Downloads) {
            return;
        }

        intervalId = setInterval(async () => {
            const retrievedQueues = await GetDownloadQueues();
            if (retrievedQueues === null) {
                downloadQueues = [];
                return;
            }

            modalLogic(modalsId, retrievedQueues, () => ({ open: false, pageNum: 1 }));
            modalLogic(progHistoryModalsId, retrievedQueues, () => false);
            modalLogic(inputModalsId, retrievedQueues, () => false);
            modalLogic(errModalsId, retrievedQueues, () => false);

            downloadQueues = [...retrievedQueues];
        }, 500);
    });

    onDestroy(() => {
        clearInterval(intervalId);
        unsubscribeAction();
    });
</script>

<div class="container mx-auto">
    <h2 class="mb-3" id="download-queue-h2">{translate("Download Queues", "download-queue-h2")}</h2>
    <Table hoverable={true} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>
                <Translate text="Date/Time" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Your Inputs" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Current Task" />
            </TableHeadCell>
            <TableHeadCell>
                <Translate text="Actions" />
            </TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if downloadQueues.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan={4}>
                        <Translate text="There are no download queues at the moment." />
                    </TableBodyCell>
                </TableBodyRow>
            {:else}
                {#each downloadQueues as dlQ}
                    <TableBodyRow>
                        <TableBodyCell>
                            <span>{makeDateTimeReadable(dlQ.ProgressBar.DateTime)}</span>
                        </TableBodyCell>
                        <TableBodyCell class="whitespace-normal text-center">
                            <Inputs {dlQ} {inputModalsId} />
                        </TableBodyCell>
                        <TableBodyCell tdClass="px-6 py-4 font-medium">
                            <Tasks {dlQ} {progHistoryModalsId} {makeDateTimeReadable} />
                        </TableBodyCell>
                        <TableBodyCell tdClass="text-center">
                            <Actions {dlQ} {modalsId} {errModalsId} />
                        </TableBodyCell>
                    </TableBodyRow>
                {/each}
            {/if}
        </TableBody>
    </Table>
</div>
