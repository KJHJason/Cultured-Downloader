<script lang="ts">
    import { Progressbar, Modal, Tooltip, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Spinner } from "flowbite-svelte";
    import { BrowserOpenURL } from "../scripts/wailsjs/runtime/runtime";
    import loadingImg from "../assets/images/bocchi-loading.gif";
    import { onMount } from "svelte";
    import { GetDownloadQueues } from "../scripts/wailsjs/go/app/App";
    import { FolderSolid, NewspaperSolid, StopSolid, TrashBinSolid, ClipboardListSolid } from "flowbite-svelte-icons";
    import { Translate, GetLocale } from "../scripts/language";

    let inputModalsId: Record<number, boolean> = {};
    let progHistoryModalsId: Record<number, boolean> = {}; 
    let modalsId: Record<number, boolean> = {};
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

    onMount(async () => {
        // make a polling request to get the download queues
        setInterval(async () => {
            const retrievedQueues = await GetDownloadQueues();
            console.log(retrievedQueues);
            if (retrievedQueues === null) {
                return;
            }

            modalLogic(modalsId, retrievedQueues);
            modalLogic(progHistoryModalsId, retrievedQueues);
            modalLogic(inputModalsId, retrievedQueues);

            downloadQueues = [...retrievedQueues];
        }, 400);
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
                    </TableBodyCell>
                    <TableBodyCell>
                        {@const success = dlQ.ProgressBar.Finished && !dlQ.ProgressBar.HasError}
                        {@const hasError = dlQ.ProgressBar.Finished && dlQ.ProgressBar.HasError}
                        <div class="flex justify-between mb-1">
                            {#if success}
                                <span class="pr-2 font-medium">{dlQ.SuccessMsg}</span>
                            {:else if hasError}
                                <span class="pr-2 font-medium">{dlQ.ErrMsg}</span>
                            {:else}
                                <span class="pr-2 font-medium">{dlQ.Msg}</span>
                            {/if}
                        </div>

                        {#if success}
                            <Progressbar progress="100" color="green" animate={true} />
                        {:else if hasError}
                            <Progressbar progress="100" color="red" animate={true} />
                        {:else if dlQ.ProgressBar.IsSpinner}
                            <Spinner color="blue" />
                        {:else}
                            <Progressbar progress="{dlQ.ProgressBar.Percentage}" color="blue" animate={true} />
                        {/if}

                        <!-- TODO: nested progress bar -->
                        {#if dlQ.NestedProgressBar.length > 0}
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
                                        {#each dlQ.NestedProgressBar as nestedProgBar}
                                            <TableBodyRow>
                                                <TableBodyCell>
                                                    {makeDateTimeReadable(nestedProgBar.DateTime, true)}
                                                </TableBodyCell>
                                                <TableBodyCell>
                                                    <div class="flex justify-between mb-1">
                                                        {#if nestedProgBar.HasError}
                                                            <span class="font-medium pr-2">{nestedProgBar.ErrMsg}</span>
                                                        {:else if nestedProgBar.Finished}
                                                            <span class="font-medium pr-2">{nestedProgBar.SuccessMsg}</span>
                                                        {:else}
                                                            <span class="font-medium pr-2">{nestedProgBar.Msg}</span>
                                                        {/if}
                                                        <span class="font-medium pr-2">{nestedProgBar.Percentage}%</span>
                                                    </div>

                                                    {#if nestedProgBar.HasError}
                                                        <Progressbar progress="{nestedProgBar.Percentage}" color="red" animate={true} />
                                                    {:else if nestedProgBar.Finished}
                                                        <Progressbar progress="100" color="green" animate={true} />
                                                    {:else}
                                                        <Progressbar progress="{nestedProgBar.Percentage}" color="blue" animate={true} />
                                                    {/if}
                                                </TableBodyCell>
                                            </TableBodyRow>
                                        {/each}
                                    </TableBody>
                                </Table>
                            </Modal>
                        {/if}
                    </TableBodyCell>

                    <TableBodyCell tdClass="text-center">
                        {#if dlQ.ProgressBar.Finished}
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
                                        {#if dlQ.DlProgressBars.length === 0}
                                            <TableBodyRow>
                                                <TableBodyCell tdClass="text-center p-3" colspan="3">
                                                    {Translate("Nothing here!")}
                                                </TableBodyCell>
                                            </TableBodyRow>
                                        {:else}
                                        {#each dlQ.DlProgressBars as dlDetails}
                                            <TableBodyRow>
                                                <TableBodyCell>
                                                    <span class="break-words">
                                                        {#if dlDetails.Filename == ""}
                                                            {Translate("Loading...")}
                                                        {:else}
                                                            {dlDetails.Filename}
                                                        {/if}
                                                    </span>
                                                </TableBodyCell>
                                                <TableBodyCell>
                                                    <span>{parseFloat(dlDetails.DownloadSpeed).toFixed(2)} MB/s</span>
                                                </TableBodyCell>
                                                <TableBodyCell>
                                                    {#if dlDetails.DownloadETA == -1}
                                                        <Spinner color="yellow" />
                                                        <span class="pl-2">{Translate("Unknown ETA...")}</span>
                                                    {:else}
                                                        <div class="flex justify-between mb-1">
                                                            <span class="font-medium pr-2">
                                                                {#if dlDetails.DownloadETA > 60}
                                                                    {(parseFloat(dlDetails.DownloadETA)/ 60).toFixed(2)} {Translate("minutes").toLocaleLowerCase()}
                                                                {:else if dlDetails.DownloadETA == 0}
                                                                    {Translate("Downloaded!")}
                                                                {:else}
                                                                    {parseFloat(dlDetails.DownloadETA).toFixed(2)} {Translate("seconds").toLocaleLowerCase()}
                                                                {/if}
                                                            </span>
                                                        </div>

                                                        {#if dlDetails.Finished}
                                                            <Progressbar progress="100" color="green" animate={true} />
                                                        {:else if dlDetails.HasError}
                                                            <Progressbar progress="100" color="red" animate={true} />
                                                        {:else}
                                                            <Progressbar progress="{dlDetails.Percentage}" color="blue" animate={true} />
                                                        {/if}
                                                    {/if}
                                                </TableBodyCell>
                                            </TableBodyRow>
                                        {/each}
                                        {/if}
                                    </TableBody>
                                </Table>
                            </Modal>
                        {/if}
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
            {/if}
        </TableBody>
    </Table>
</div>
