<script lang="ts">
    import { Label, Select, Input, Toggle } from "flowbite-svelte";

    let pixivArtworkType = 3;
    const pixivArtworkTypes = [
        { value: 1, name: "Illustrations and Ugoira" },
        { value: 2, name: "Manga" },
        { value: 3, name: "All" }
    ];
    let pixivRating = 6;
    const pixivRatings = [
        { value: 4, name: "R-18" },
        { value: 5, name: "Safe" },
        { value: 6, name: "All" }
    ];
    let pixivSearchMode = 9;
    const pixivSearchModes = [
        { value: 7, name: "Similar Tag Names" },
        { value: 8, name: "Tags" },
        { value: 9, name: "Title and Caption" },
    ];
    let pixivSortOrder = 10;
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
    let pixivUgoiraFormat = 18;
    const pixivUgoiraFormats = [
        { value: 18, name: ".gif" },
        { value: 19, name: ".apng" },
        { value: 20, name: ".webp" },
        { value: 21, name: ".webm" },
        { value: 22, name: ".mp4" },
    ];
</script>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="md:col-span-2 mt-4">
        <Toggle color="green" name="DeleteUgoiraZip">Delete Ugoira Zip</Toggle>
    </div>
    <div>
        <Label for="ArtworkType">Artwork Type:</Label>
        <Select 
            class="mt-2" 
            name="ArtworkType" 
            id="ArtworkType" 
            items={pixivArtworkTypes} 
            bind:value={pixivArtworkType} 
        />
    </div>
    <div>
        <Label for="RatingMode">Rating Mode:</Label>
        <Select 
            class="mt-2" 
            name="RatingMode" 
            id="RatingMode" 
            items={pixivRatings} 
            bind:value={pixivRating} 
        />
    </div>
    <div>
        <Label for="SearchMode">Search Mode:</Label>
        <Select 
            class="mt-2" 
            name="SearchMode" 
            id="SearchMode" 
            items={pixivSearchModes} 
            bind:value={pixivSearchMode} 
        />
    </div>
    <div>
        <Label for="SortOrder">Sort Order:</Label>
        <Select 
            class="mt-2" 
            name="SortOrder" 
            id="SortOrder" 
            items={pixivSortOrders} 
            bind:value={pixivSortOrder} 
        />
    </div>
    <div>
        <Label for="UgoiraOutputFormat">Ugoira Output File Format:</Label>
        <Select 
            class="mt-2" 
            name="UgoiraOutputFormat" 
            id="UgoiraOutputFormat" 
            items={pixivUgoiraFormats} 
            bind:value={pixivUgoiraFormat} 
        />
    </div>
    <div>
        <Label for="UgoiraQuality">Ugoira Quality:</Label>
        <Input 
            class="mt-2" 
            name="UgoiraQuality" 
            id="UgoiraQuality" 
            type="number"
            placeholder="0-51 for mp4, 0-63 for webm"
        />
    </div>
</div>
