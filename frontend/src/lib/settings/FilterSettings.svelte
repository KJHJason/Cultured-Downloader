<script lang="ts">
    import { Helper, AccordionItem, Accordion, Label, Textarea, Input, InputAddon, ButtonGroup, Tooltip } from "flowbite-svelte";
	import { DateInput } from "date-picker-svelte"
    import { onMount } from "svelte";
    import { InfoCircleSolid } from "flowbite-svelte-icons";
    import { translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";

    export let minFileSize: number = 0;
    export let maxFileSize: number | null = Infinity;
    export let postDateRange: Record<string, null | Date> = { from: null, to: null };
    export let fileExtensions: string = "";
    export let filenameRegex: string = "";

    const now = new Date();

    $: maxFileSizePlaceholder = "";
    $: fileExtTextAreaPlaceholder = "";
    $: fileExtTextareaExample = "";
    $: filenameRegexPlaceholder = "";
    $: filenameRegexTooltipInfo = "";
    onMount(async () => {
        maxFileSizePlaceholder = await translateText("Leave it empty for infinity");
        fileExtTextAreaPlaceholder = await translateText("Leave it empty or separate it with newlines like the following...");
        fileExtTextareaExample = (await translateText("jpg<>zip<>psd")).replaceAll("<>", "\n");
        filenameRegexPlaceholder = await translateText("Leave it empty or add your own regex!");
        filenameRegexTooltipInfo = await translateText("Will only download the file if there were any matches in the filename using your regex.");
    });
</script>

<Accordion class="mt-2" inactiveClass="bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-100 hover:dark:bg-gray-800">
    <AccordionItem tag="h4" borderOpenClass="border-s border-e bg-gray-100 dark:bg-gray-800 rounded-b-lg">
        <Translate text="Filter Settings" slot="header" />
        <form id="dl-filter-settings-form">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <Label for="StartDate">
                        <Translate text="Start Date:" />
                    </Label>
                    <DateInput 
                        id="StartDate" 
                        class="mt-2" 
                        closeOnSelection 
                        bind:value={postDateRange.from} 
                        format="yyyy-MM-dd"
                        max={now} 
                    />
                </div>
                <div>
                    <Label for="EndDate">
                        <Translate text="End Date:" />
                    </Label>
                    <DateInput 
                        id="EndDate" 
                        class="mt-2" 
                        closeOnSelection 
                        bind:value={postDateRange.to} 
                        format="yyyy-MM-dd"
                        max={now} 
                    />
                </div>
                <div>
                    <Label for="MinFileSize">
                        <Translate text="Mininum File Size:" />
                    </Label>
                    <ButtonGroup class="w-full mt-2">
                        <Input id="MinFileSize" name="MinFileSize" placeholder="0" min={0} type="number" bind:value={minFileSize} required={true} />
                        <InputAddon>
                            MB
                        </InputAddon>
                    </ButtonGroup>
                </div>
                <div>
                    <Label for="MaxFileSize">
                        <Translate text="Maximum File Size:" />
                    </Label>
                    <ButtonGroup class="w-full mt-2">
                        <Input id="MaxFileSize" name="MaxFileSize" placeholder="{maxFileSizePlaceholder}" type="number" bind:value={maxFileSize} />
                        <InputAddon class="font-bold">
                            MB
                        </InputAddon>
                    </ButtonGroup>
                </div>
                <div>
                    <Label for="FileExtensions" class="mb-2">
                        <Translate text="File Extensions:" />
                    </Label>
                    <Textarea 
                        id="FileExtensions"
                        name="FileExtensions"
                        rows={5}
                        bind:value={fileExtensions}
                        placeholder={fileExtTextAreaPlaceholder + "\n" + fileExtTextareaExample}
                    />
                </div>
                <div>
                    <div class="flex mb-2">
                        <Label for="FilenameRegex">
                            <Translate text="Filename Regex:" />
                        </Label>
                        <button type="button" class="btn-text-link ml-2" id="filename-regex-info">
                            <InfoCircleSolid />
                        </button>
                        <Tooltip class="max-w-md" triggeredBy="#filename-regex-info">
                            {filenameRegexTooltipInfo}
                        </Tooltip>
                    </div>
                    <Textarea 
                        id="FilenameRegex"
                        name="FilenameRegex"
                        rows={3}
                        bind:value={filenameRegex}
                        placeholder={filenameRegexPlaceholder + "\n" + "Example: ^[a-zA-Z0-9]+\\_(rakugaki-chan)"}
                    />
                    <Helper>
                        <Translate text="Tip: You can test your regex at regex101.com (Golang)." />
                    </Helper>
                </div>
            </div>
        </form>
    </AccordionItem>
</Accordion>
