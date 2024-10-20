<script lang="ts">
    import { Modal, Label, Textarea, Input, Toggle, Spinner, InputAddon, ButtonGroup } from "flowbite-svelte";
    
	import { DateInput } from 'date-picker-svelte'
	let date = new Date()

    import { writable } from "svelte/store";
    import { onMount } from "svelte";
    import { FilterOutline } from "flowbite-svelte-icons";
    import { translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";

    let open: boolean;

    let minFileSize: number = 0;
    let maxFileSize: number = Infinity;
    let postDateRange: Record<string, null | Date> = { from: null, to: null };

    const initFilterValues = async () => {

    };

    $: modalTitle = "";
    $: maxFileSizePlaceholder = "";
    $: fileExtTextAreaPlaceholder = "";
    $: fileExtTextareaExample = "";
    $: filenameRegexPlaceholder = "";
    onMount(async () => {
        modalTitle = await translateText("Filter Settings");
        maxFileSizePlaceholder = await translateText("Leave empty for infinity");
        fileExtTextAreaPlaceholder = await translateText("Leave it empty or separate it with newlines like the following...");
        fileExtTextareaExample = (await translateText("jpg<>zip<>psd")).replaceAll("<>", "\n");
        filenameRegexPlaceholder = await translateText("Leave it empty or add your own regex!")
    });
</script>

<!-- MinFileSize:    0,
MaxFileSize:    0,
FileExt:        []string{},
StartDate:      time.Time{},
EndDate:        time.Time{},
FileNameFilter: nil, -->
<Modal bind:open={open} title="{modalTitle}" id="view-filter-settings" size="lg" autoclose={false}>
    <form id="dl-filter-settings-form" class="min-h-[250px]">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {#await initFilterValues()}
                <div class="flex">
                    <Spinner color="blue" />
                    <p class="ms-3">
                        <Translate text="Loading the rest of the form..." />
                    </p>
                </div>
            {:then}
                <div>
                    <Label for="StartDate">
                        <Translate text="Start Date:" />
                    </Label>
                    <DateInput id="StartDate" class="mt-2" closeOnSelection bind:value={postDateRange.from} format="yyyy-MM-dd" />
                </div>
                <div>
                    <Label for="EndDate">
                        <Translate text="End Date:" />
                    </Label>
                    <DateInput id="EndDate" class="mt-2" closeOnSelection bind:value={postDateRange.to} format="yyyy-MM-dd" />
                </div>
                <div>
                    <Label for="MinFileSize">
                        <Translate text="Mininum File Size:" />
                    </Label>
                    <ButtonGroup class="w-full mt-2">
                        <Input id="MinFileSize" name="MinFileSize" placeholder="0" type="number" value={minFileSize} required={true} />
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
                        <Input id="MaxFileSize" name="MaxFileSize" placeholder="{maxFileSizePlaceholder}" type="number" value={maxFileSize} />
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
                        placeholder={fileExtTextAreaPlaceholder + "\n" + fileExtTextareaExample}
                    />
                </div>
                <div>
                    <Label for="FilenameRegex" class="mb-2">
                        <Translate text="Filename Regex:" />
                    </Label>
                    <Textarea 
                        id="FilenameRegex"
                        name="FilenameRegex"
                        rows={3}
                        placeholder={filenameRegexPlaceholder + "\n" + "Example: ^\\w+\\.(zip|rar|7z)$"}
                    />
                </div>
            {/await}
        </div>
    </form>
</Modal>


<div class="mt-5">
    <button type="button" class="btn btn-warning flex" on:click={() => open = true} >
        <div class="text-main">
            <FilterOutline />
        </div>
        <Translate text="Filter Settings" />
    </button>
</div>
