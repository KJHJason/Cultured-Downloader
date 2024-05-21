<script lang="ts">
    import { Label, Select, Input, Toggle, Helper, Spinner, Tooltip } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { GetPreferences, SetPixivPreferences } from "../../scripts/wailsjs/go/app/App";
    import { pixivFormId, swal } from "../../scripts/constants";
    import { translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";
    import { InfoCircleSolid } from "flowbite-svelte-icons";
    import type { app } from "../../scripts/wailsjs/go/models";

    export let formId = pixivFormId;
    export let promptSuccess: boolean;
    export let preferences: app.Preferences | undefined = undefined;
    export let pixivArtworkType: number = 3;

    type selectValues = { value: number, name: string }[];
    const pixivArtworkTypes: selectValues = [];
    const initPixivArtworkTypes = async () => {
        pixivArtworkTypes.push({
            value: 1,
            name: await translateText("Illustrations and Ugoira")
        });
        pixivArtworkTypes.push({
            value: 2,
            name: await translateText("Manga")
        });
        pixivArtworkTypes.push({
            value: 3,
            name: await translateText("All")
        });
    };

    export let pixivRating: number = 6;
    const pixivRatings: selectValues = [];
    const initPixivRatings = async () => {
        pixivRatings.push({
            value: 4,
            name: await translateText("R-18")
        });
        pixivRatings.push({
            value: 5,
            name: await translateText("Safe")
        });
        pixivRatings.push({
            value: 6,
            name: await translateText("All")
        });
    };

    export let pixivSearchMode: number = 8;
    const pixivSearchModes: selectValues = [];
    const initPixivSearchModes = async () => {
        pixivSearchModes.push({
            value: 7,
            name: await translateText("Similar Tag Names")
        });
        pixivSearchModes.push({
            value: 8,
            name: await translateText("Tags")
        });
        pixivSearchModes.push({
            value: 9,
            name: await translateText("Title and Caption")
        });
    };

    export let pixivSortOrder: number = 10;
    const pixivSortOrders: selectValues = [];
    const initPixivSortOrders = async () => {
        pixivSortOrders.push({
            value: 10,
            name: await translateText("By Date")
        });
        pixivSortOrders.push({
            value: 11,
            name: await translateText("By Date (Descending)")
        });
        pixivSortOrders.push({
            value: 12,
            name: await translateText("By Popularity")
        });
        pixivSortOrders.push({
            value: 13,
            name: await translateText("By Popularity (Descending)")
        });
        pixivSortOrders.push({
            value: 14,
            name: await translateText("By Popularity (Male)")
        });
        pixivSortOrders.push({
            value: 15,
            name: await translateText("By Popularity (Descending/Male)")
        });
        pixivSortOrders.push({
            value: 16,
            name: await translateText("By Popularity (Female)")
        });
        pixivSortOrders.push({
            value: 17,
            name: await translateText("By Popularity (Descending/Female)")
        });
    };

    export let pixivUgoiraFormat: number = 18;
    const pixivUgoiraFormats = [
        { value: 18, name: ".gif" },
        { value: 19, name: ".apng" },
        { value: 20, name: ".webp" },
        { value: 21, name: ".webm" },
        { value: 22, name: ".mp4" },
    ];

    export let pixivAiSearchMode: number = 24;
    const pixivAiSearchModes: selectValues = [];
    const initPixivAiSearchModes = async () => {
        pixivAiSearchModes.push({
            value: 23,
            name: await translateText("Display AI Works")
        });
        pixivAiSearchModes.push({
            value: 24,
            name: await translateText("Filter AI Works")
        });
    };

    const initSelectValues = async () => {
        await initPixivArtworkTypes();
        await initPixivRatings();
        await initPixivSearchModes();
        await initPixivSortOrders();
        await initPixivAiSearchModes();
    };

    let DeleteUgoiraZipInp: HTMLInputElement;
    let UgoiraQualityInp: HTMLInputElement;
    const processPrefs = (preferences: app.Preferences) => {
        DeleteUgoiraZipInp.checked = preferences.DeleteUgoiraZip;
        pixivArtworkType           = preferences.ArtworkType;
        pixivRating                = preferences.RatingMode;
        pixivSearchMode            = preferences.SearchMode;
        pixivAiSearchMode          = preferences.AiSearchMode;
        pixivSortOrder             = preferences.SortOrder;
        pixivUgoiraFormat          = preferences.UgoiraOutputFormat;
        UgoiraQualityInp.value     = preferences.UgoiraQuality.toString();
    };

    onMount(async() => {
        // Pixiv Specific
        DeleteUgoiraZipInp = document.getElementById("DeleteUgoiraZip") as HTMLInputElement;
        UgoiraQualityInp = document.getElementById("UgoiraQuality") as HTMLInputElement;

        if (preferences === undefined) {
            preferences = await GetPreferences();
        }
        processPrefs(preferences);

        const success = await translateText("Success");
        const prefsSaved = await translateText("Preferences saved successfully");

        const prefForm = document.getElementById(formId) as HTMLFormElement;
        prefForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const prefs: app.PixivPreferences = {
                DeleteUgoiraZip:    DeleteUgoiraZipInp.checked,
                ArtworkType:        pixivArtworkType,
                RatingMode:         pixivRating,
                SearchMode:         pixivSearchMode,
                AiSearchMode:       pixivAiSearchMode,
                SortOrder:          pixivSortOrder,
                UgoiraOutputFormat: pixivUgoiraFormat,
                UgoiraQuality:      parseInt(UgoiraQualityInp.value),
            };
            await SetPixivPreferences(prefs);
            processPrefs(await GetPreferences());

            if (promptSuccess) {
                swal.fire({
                    title: success,
                    text: prefsSaved,
                    icon: "success",
                });
            }
        });
    });

    let deleteUgoiraZipInfo = "";
    let ugoiraQualityInfo = "";
    onMount(async () => {
        deleteUgoiraZipInfo = await translateText("Delete the downloaded Ugoira zip file containing the original image frames after converting it into a usable format via FFmpeg.");
        ugoiraQualityInfo = await translateText("A lower value would result in better quality but longer conversion times. The range is 0-51 for mp4 and 0-63 for webm. The recommended value is around 10 to balance between quality and conversion time.");
    });
</script>

<form id={formId}>
    <div class="grid grid-cols-1 md:grid-cols-2 my-4">
        <Toggle color="green" id="DeleteUgoiraZip" name="DeleteUgoiraZip">
            <Translate text="Delete Ugoira Zip After Conversion" />
            <button type="button" class="btn-text-link ml-2" id="delete-ugoira-zip-info">
                <InfoCircleSolid />
            </button>
            <Tooltip class="max-w-md" triggeredBy="#delete-ugoira-zip-info">
                {deleteUgoiraZipInfo}
            </Tooltip>
        </Toggle>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {#await initSelectValues()}
            <div class="flex">
                <Spinner color="blue" />
                <p class="ms-3">
                    <Translate text="Loading the rest of the form..." />
                </p>
            </div>
        {:then}
            <div>
                <Label for="ArtworkType">
                    <Translate text="Artwork Type:" />
                </Label>
                <Select 
                    class="mt-2" 
                    name="ArtworkType" 
                    id="ArtworkType" 
                    items={pixivArtworkTypes} 
                    bind:value={pixivArtworkType} 
                />
            </div>
            <div>
                <Label for="RatingMode">
                    <Translate text="Rating Mode:" />
                </Label>
                <Select 
                    class="mt-2" 
                    name="RatingMode" 
                    id="RatingMode" 
                    items={pixivRatings} 
                    bind:value={pixivRating} 
                />
            </div>
            <div>
                <Label for="SearchMode">
                    <Translate text="Search Mode:" />
                </Label>
                <Select 
                    class="mt-2" 
                    name="SearchMode" 
                    id="SearchMode" 
                    items={pixivSearchModes} 
                    bind:value={pixivSearchMode} 
                />
            </div>
            <div>
                <Label for="AiSearchMode">
                    <Translate text="AI Search Mode:" />
                </Label>
                <Select 
                    class="mt-2" 
                    name="AiSearchMode" 
                    id="AiSearchMode" 
                    items={pixivAiSearchModes} 
                    bind:value={pixivAiSearchMode} 
                />
            </div>
            <div>
                <Label for="SortOrder">
                    <Translate text="Sort Order:" />
                </Label>
                <Select 
                    class="mt-2" 
                    name="SortOrder" 
                    id="SortOrder" 
                    items={pixivSortOrders} 
                    bind:value={pixivSortOrder} 
                />
            </div>
            <div>
                <Label for="UgoiraOutputFormat">
                    <Translate text="Ugoira Output File Format:" />
                </Label>
                <Select 
                    class="mt-2" 
                    name="UgoiraOutputFormat" 
                    id="UgoiraOutputFormat" 
                    items={pixivUgoiraFormats} 
                    bind:value={pixivUgoiraFormat} 
                />
            </div>
        {/await}
        <div>
            <div class="flex">
                <Label for="UgoiraQuality">
                    <Translate text="Ugoira Quality:" />
                </Label>
                <button type="button" class="btn-text-link ml-2" id="ugoira-quality-info">
                    <InfoCircleSolid />
                </button>
                <Tooltip class="max-w-md" triggeredBy="#ugoira-quality-info">
                    {ugoiraQualityInfo}
                </Tooltip>
            </div>
            <Input 
                class="mt-2" 
                name="UgoiraQuality" 
                id="UgoiraQuality" 
                type="number"
                placeholder="0-51 for mp4, 0-63 for webm"
                min="0"
                max="63"
            />
        </div>
    </div>
</form>
