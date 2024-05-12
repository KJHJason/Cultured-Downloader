<script lang="ts">
    import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";
    import { SubmitPixivToQueue, ValidatePixivInputs } from "../scripts/wailsjs/go/app/App";

    const urlValidationFn = async (urls: string | string[]): Promise<boolean> => {
        if (typeof urls === "string") {
            urls = urls.split("\n");
        }
        return await ValidatePixivInputs(urls);
    };

    const addToQueueFn = async (inputs: string[], options: Record<string, any>): Promise<void> => {
        await SubmitPixivToQueue(inputs, options);
    };

    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return !(inputUrl.startsWith("https://www.pixiv.net/en/artworks") || inputUrl.startsWith("https://www.pixiv.net/artworks"));
    };
</script>

<PlatformBase
    platformName={actions.Pixiv}
    inputPlaceholder={`Mika Misono
らくがきちゃん
https://www.pixiv.net/artworks/113096188
https://www.pixiv.net/en/artworks/113096160
https://www.pixiv.net/en/users/10600906`}
    {urlValidationFn}
    {checkUrlHasPageNumFilter}
    {addToQueueFn}
/>
