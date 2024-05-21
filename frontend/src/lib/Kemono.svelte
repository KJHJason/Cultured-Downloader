<script lang="ts">
    import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";
    import { ValidateKemonoInputs, SubmitKemonoToQueue } from "../scripts/wailsjs/go/app/App";
    import type { app } from "../scripts/wailsjs/go/models";

    const urlValidationFn = async (urls: string | string[]): Promise<boolean> => {
        if (typeof urls === "string") {
            urls = urls.split("\n");
        }
        return await ValidateKemonoInputs(urls);
    };

    const addToQueueFn = async (inputs: string[], options: app.Preferences): Promise<void> => {
        await SubmitKemonoToQueue(inputs, options);
    };

    const creatorUrlRegex = /^https:\/\/kemono.su\/(?:patreon|fanbox|gumroad|subscribestar|dlsite|fantia|boosty)\/user\/\d+$/;
    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return creatorUrlRegex.test(inputUrl);
    };
</script>

<PlatformBase 
    platformName={actions.Kemono}
    inputPlaceholder={`favorites
favourites
https://kemono.su/patreon/user/42628911
https://kemono.su/patreon/user/42628911/post/98584740`}
    {urlValidationFn}
    {addToQueueFn}
    {checkUrlHasPageNumFilter}
/>
