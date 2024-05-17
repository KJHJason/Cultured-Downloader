<script lang="ts">
    import { Label, Select, Input, Toggle, Helper } from "flowbite-svelte";
    import { onMount } from "svelte";
    import { GetPreferences, SetPixivPreferences } from "../../scripts/wailsjs/go/app/App";
    import { pixivFormId, swal } from "../../scripts/constants";
    import { translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";

    export let formId = pixivFormId;
    export let promptSuccess: boolean;
    export let preferences: any = undefined;

    export let pixivArtworkType: number = 3;
    const pixivArtworkTypes = [
        { value: 1, name: "Illustrations and Ugoira" },
        { value: 2, name: "Manga" },
        { value: 3, name: "All" }
    ];
    export let pixivRating: number = 6;
    const pixivRatings = [
        { value: 4, name: "R-18" },
        { value: 5, name: "Safe" },
        { value: 6, name: "All" }
    ];
    export let pixivSearchMode: number = 8;
    const pixivSearchModes = [
        { value: 7, name: "Similar Tag Names" },
        { value: 8, name: "Tags" },
        { value: 9, name: "Title and Caption" },
    ];
    export let pixivSortOrder: number = 10;
    const pixivSortOrders = [
        { value: 10, name: "By Date" },
        { value: 11, name: "By Date (Descending)" },
        { value: 12, name: "By Popularity" },
        { value: 13, name: "By Popularity (Descending)" },
        { value: 14, name: "By Popularity (Male)" },
        { value: 15, name: "By Popularity (Descending/Male)" },
        { value: 16, name: "By Popularity (Female)" },
        { value: 17, name: "By Popularity (Descending/Female)" },
    ];
    export let pixivUgoiraFormat: number = 18;
    const pixivUgoiraFormats = [
        { value: 18, name: ".gif" },
        { value: 19, name: ".apng" },
        { value: 20, name: ".webp" },
        { value: 21, name: ".webm" },
        { value: 22, name: ".mp4" },
    ];
    export let pixivAiSearchMode: number = 24;
    const pixivAiSearchModes = [
        { value: 23, name: "Display AI Works" },
        { value: 24, name: "Filter AI Works" },
    ];

    let DeleteUgoiraZipInp: HTMLInputElement;
    let UgoiraQualityInp: HTMLInputElement;
    const processPrefs = (preferences: any) => {
        DeleteUgoiraZipInp.checked = preferences.DeleteUgoiraZip;
        pixivArtworkType           = preferences.ArtworkType;
        pixivRating                = preferences.RatingMode;
        pixivSearchMode            = preferences.SearchMode;
        pixivAiSearchMode          = preferences.AiSearchMode;
        pixivSortOrder             = preferences.SortOrder;
        pixivUgoiraFormat          = preferences.UgoiraOutputFormat;
        UgoiraQualityInp.value     = preferences.UgoiraQuality;
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
            const prefs = {
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
</script>

<form id={formId}>
    <div class="grid grid-cols-1 md:grid-cols-2 my-4">
        <Toggle color="green" id="DeleteUgoiraZip" name="DeleteUgoiraZip">
            <Translate text="Delete Ugoira Zip After Conversion" />
        </Toggle>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
        <div>
            <Label for="UgoiraQuality">
                <Translate text="Ugoira Quality:" />
            </Label>
            <Input 
                class="mt-2" 
                name="UgoiraQuality" 
                id="UgoiraQuality" 
                type="number"
                placeholder="0-51 for mp4, 0-63 for webm"
                min="0"
                max="63"
            />
            <Helper class="mt-1">
                <Translate text="Lower values mean better quality but longer conversion times!" />
            </Helper>
        </div>
    </div>
</form>
