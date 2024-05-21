<script lang="ts">
    import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";
    import { ValidatePixivFanboxUrls, SubmitPixivFanboxToQueue } from "../scripts/wailsjs/go/app/App";
    import type { app } from "../scripts/wailsjs/go/models";

    const urlValidationFn = async (urls: string | string[]): Promise<boolean> => {
        if (typeof urls === "string") {
            urls = urls.split("\n");
        }
        return await ValidatePixivFanboxUrls(urls);
    };

    const addToQueueFn = async (inputs: string[], options: app.Preferences): Promise<void> => {
        await SubmitPixivFanboxToQueue(inputs, options);
    };

    const pixivCreatorRegex1 = /^https:\/\/[\w&.-]+.fanbox.cc(\/(posts)?)?$/;
    const pixivCreatorRegex2 = /^https:\/\/www.fanbox.cc\/@[\w&.-]+(\/posts)?$/;
    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return pixivCreatorRegex2.test(inputUrl) || pixivCreatorRegex1.test(inputUrl);
    };
</script>

<PlatformBase
    platformTitle="Pixiv Fanbox"
    platformName={actions.PixivFanbox}
    inputPlaceholder={`https://karutamo.fanbox.cc/
https://karutamo.fanbox.cc/posts/3542241
https://www.fanbox.cc/@mmafu
https://www.fanbox.cc/@mmafu/posts/7117892`} 
    {urlValidationFn}
    {addToQueueFn}
    {checkUrlHasPageNumFilter}
/>
