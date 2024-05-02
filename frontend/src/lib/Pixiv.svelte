<script lang="ts">
    import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";
    import { Toggle, Select, Helper, Input, ButtonGroup } from "flowbite-svelte";
    import { MinusOutline, PlusOutline } from "flowbite-svelte-icons";

    const urlValidationFn = (urls: string | string[]): Promise<boolean> => {
        // if (typeof urls === "string") {
        //     urls = urls.split("\n");
        // }
        // const urlRegex = /^https:\/\/fantia.jp\/(posts|fanclubs)\/\d+$/;
        // for (const url of urls) {
        //     if (!urlRegex.test(url)) {
        //         return false;
        //     }
        // }
        // return true;
        return new Promise((resolve) => {
            resolve(true);
        });
    };

    let test = "";

    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return inputUrl.startsWith("https://fantia.jp/fanclubs/");
    };
</script>

<!-- <PlatformBase 
    platformName={actions.Pixiv}
    inputPlaceholder={"Eyjafjalla\nhttps://www.pixiv.net/en/artworks/113096160\nhttps://www.pixiv.net/en/users/10600906\nhttps://www.pixiv.net/artworks/113096188"} 
    urlValidationFn={urlValidationFn}
    checkUrlHasPageNumFilter={checkUrlHasPageNumFilter}
    addToQueueFn={() => {}}
>
    <Toggle color="green" name="DeleteUgoiraZip">Delete Ugoira Zip</Toggle>
</PlatformBase> -->

<ButtonGroup class="w-full">
    <Input id="website-admin" placeholder="elonmusk" />
    <Select 
        class="rounded-r-lg !rounded-l-none" 
        name="SortOrder" 
        id="SortOrder" 
        items={[]} 
        bind:value={test} 
    />
</ButtonGroup>
<div class="mt-2 text-right">
    <Helper id="url-helper" color="red" />
    <button type="button" class="mt-2 btn btn-success" id="">
        <PlusOutline />
    </button>
    <button type="button" class="mt-2 btn btn-success" id="">
        <MinusOutline />
    </button>
</div>
