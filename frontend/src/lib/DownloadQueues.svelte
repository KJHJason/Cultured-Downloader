<script lang="ts">
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { onDestroy } from "svelte";
    import { GetDownloadQueues } from "../scripts/wailsjs/go/app/App";
    import { Translate, GetLocale } from "../scripts/language";
    import Inputs from "./queues/Inputs.svelte";
    import Tasks from "./queues/Tasks.svelte";
    import Actions from "./queues/Actions.svelte";
    import { actions } from "../scripts/constants";
    import type { Writable } from "svelte/store";

    export let action: Writable<string>;

    let inputModalsId: Record<number, boolean> = {};
    let progHistoryModalsId: Record<number, boolean> = {}; 
    let modalsId: Record<number, boolean> = {};
    let errModalsId: Record<number, boolean> = {};
    let downloadQueues: any[] = [];

    const modalLogic = (oldRecord: Record<number, boolean>, queues: Record<any, any>): void => {
        let activeId: number = -1;
        let newModalsId: Record<number, boolean> = {};
        for (const key in oldRecord) {
            if (oldRecord[key]) {
                newModalsId[key] = true;
                activeId = parseInt(key);
                break;
            }
        }
        for (const key in queues) {
            const id = queues[key].Id;
            if (activeId !== -1 && id === activeId) {
                continue;
            }
            newModalsId[id] = false;
        }
        oldRecord = newModalsId;
    };

    const makeDateTimeReadable = (dateTime: string, addSeconds: boolean = false): string => {
        const date = new Date(dateTime);
        const options: Intl.DateTimeFormatOptions = {
            month: "short", day: "numeric", 
            hour: "numeric", minute: "numeric",
        };

        if (addSeconds) {
            options.second = "numeric";
        }
        return date.toLocaleString(GetLocale(), options);
    };

    // make a polling request to get the download queues
    let intervalId: number;    
    const unsubscribeAction = action.subscribe((curAction: string) => {
        if (curAction !== actions.Downloads) {
            return;
        }

        intervalId = setInterval(async () => {
            const retrievedQueues = await GetDownloadQueues();
            console.log(retrievedQueues);
            if (retrievedQueues === null) {
                return;
            }

            modalLogic(modalsId, retrievedQueues);
            modalLogic(progHistoryModalsId, retrievedQueues);
            modalLogic(inputModalsId, retrievedQueues);
            modalLogic(errModalsId, retrievedQueues);

            downloadQueues = [...retrievedQueues];
        }, 500);
    });

    onDestroy(() => {
        clearInterval(intervalId);
        unsubscribeAction();
    });
</script>

<div class="container mx-auto">
    <h2 class="mb-3">{Translate("Download Queues")}</h2>
    <Table hoverable={true} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>{Translate("Date/Time")}</TableHeadCell>
            <TableHeadCell>{Translate("Your Inputs")}</TableHeadCell>
            <TableHeadCell>{Translate("Current Task")}</TableHeadCell>
            <TableHeadCell>{Translate("Actions")}</TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            {#if downloadQueues.length === 0}
                <TableBodyRow>
                    <TableBodyCell tdClass="text-center p-3" colspan="4">
                        {Translate("There are no download queues at the moment.")}
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
