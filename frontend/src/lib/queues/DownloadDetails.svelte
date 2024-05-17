<script lang="ts">
    import { Progressbar, TableBodyCell, TableBodyRow, Spinner } from "flowbite-svelte";
    import { convertMinsToMinsAndSecs } from "../../scripts/time";
    import Translate from "../common/Translate.svelte";
    import { onMount } from "svelte";
    import { translateText } from "../../scripts/language";

    export let dlDetails: any;

    $: translatedMins = "";
    $: translatedSecs = "";

    onMount(async () => {
        translatedMins = (await translateText("minutes")).toLocaleLowerCase();
        translatedSecs = (await translateText("seconds")).toLocaleLowerCase();
    });

    const convertSecondsToMinsAndSecs = (minutes: number): string => {
        const [mins, secs] = convertMinsToMinsAndSecs(minutes);
        return `${mins} ${translatedMins} ${secs} ${translatedSecs}`;
    }
</script>

<TableBodyRow>
    <TableBodyCell>
        {#if dlDetails.Filename == ""}
            <Translate spanClass="break-words" text="Loading..." />
        {:else}
            <span class="break-words">
                {dlDetails.Filename}
            </span>
        {/if}
    </TableBodyCell>
    <TableBodyCell>
        {dlDetails.FileSize}
    </TableBodyCell>
    <TableBodyCell>
        <span>{parseFloat(dlDetails.DownloadSpeed).toFixed(2)} MB/s</span>
    </TableBodyCell>
    <TableBodyCell>
        {#if !dlDetails.Finished && dlDetails.DownloadETA == -1}
            <Spinner color="yellow" />
            <Translate spanClass="pl-2" text="Unknown ETA..." />
        {:else}
            <div class="flex justify-between mb-1">
                <span class="font-medium pr-2">
                    {#if dlDetails.HasError}
                        {dlDetails.ErrMsg}
                    {:else if dlDetails.Finished || dlDetails.DownloadETA == 0}
                        {dlDetails.SuccessMsg}
                    {:else if dlDetails.DownloadETA > 60}
                        {convertSecondsToMinsAndSecs(dlDetails.DownloadETA / 60)}
                    {:else}
                        {parseFloat(dlDetails.DownloadETA).toFixed(2)} {translatedSecs}
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
