<script lang="ts">
    import { Progressbar, TableBodyCell, TableBodyRow, Spinner } from "flowbite-svelte";
    import { Translate } from "../../scripts/language";
    import { convertMinsToMinsAndSecs } from "../../scripts/time";

    export let dlDetails: any;

    const convertSecondsToMinsAndSecs = (minutes: number): string => {
        const [mins, secs] = convertMinsToMinsAndSecs(minutes);
        return `${mins} ${Translate("minutes").toLocaleLowerCase()} ${secs} ${Translate("seconds").toLocaleLowerCase()}`;
    }
</script>

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
        {#if !dlDetails.Finished && dlDetails.DownloadETA == -1}
            <Spinner color="yellow" />
            <span class="pl-2">{Translate("Unknown ETA...")}</span>
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
