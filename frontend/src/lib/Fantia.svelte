<script lang="ts">
    import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";
    import { ValidateFantiaUrls, SubmitFantiaToQueue } from "../scripts/wailsjs/go/app/App";
    import type { app } from "../scripts/wailsjs/go/models";

    const urlValidationFn = async (urls: string | string[]): Promise<boolean> => {
        if (typeof urls === "string") {
            urls = urls.split("\n");
        }
        return await ValidateFantiaUrls(urls);
    };

    const addToQueueFn = async (inputs: string[], options: app.Preferences): Promise<void> => {
        await SubmitFantiaToQueue(inputs, options);
    };

    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return inputUrl.startsWith("https://fantia.jp/fanclubs/");
    };
</script>

<PlatformBase 
    platformName={actions.Fantia}
    inputPlaceholder={`https://fantia.jp/posts/2239524
https://fantia.jp/products/32490
https://fantia.jp/fanclubs/5744
https://fantia.jp/fanclubs/5744/products`} 
    {urlValidationFn}
    {addToQueueFn}
    {checkUrlHasPageNumFilter}
/>
