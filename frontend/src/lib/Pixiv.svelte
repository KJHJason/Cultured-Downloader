<script lang="ts">
    import { Toggle } from "flowbite-svelte";
import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";

    const urlValidationFn = (urls: string | string[]): boolean => {
        if (typeof urls === "string") {
            urls = urls.split("\n");
        }
        const urlRegex = /^https:\/\/fantia.jp\/(posts|fanclubs)\/\d+$/;
        for (const url of urls) {
            if (!urlRegex.test(url)) {
                return false;
            }
        }
        return true;
    };

    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return inputUrl.startsWith("https://fantia.jp/fanclubs/");
    };
</script>

<PlatformBase 
    platformName={actions.Pixiv}
    inputPlaceholder={"Eyjafjalla\nhttps://www.pixiv.net/en/artworks/113096160\nhttps://www.pixiv.net/en/users/10600906\nhttps://www.pixiv.net/artworks/113096188"} 
    urlValidationFn={urlValidationFn}
    checkUrlHasPageNumFilter={checkUrlHasPageNumFilter}
>
    <Toggle color="green" name="DeleteUgoiraZip">Delete Ugoira Zip</Toggle>
</PlatformBase>
