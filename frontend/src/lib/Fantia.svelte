<script lang="ts">
    import { actions } from "../scripts/constants";
    import PlatformBase from "./PlatformBase.svelte";
    import { Toggle } from "flowbite-svelte";

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
    platformName={actions.Fantia}
    inputPlaceholder={"https://fantia.jp/posts/2239524\nhttps://fantia.jp/fanclubs/5744"} 
    urlValidationFn={urlValidationFn}
    checkUrlHasPageNumFilter={checkUrlHasPageNumFilter}
>
    <Toggle color="green" name="DlGDrive">GDrive Links</Toggle>
    <Toggle color="green" name="DetectOtherLinks">Detect Other URL(s) like MEGA</Toggle>
    <Toggle color="green" name="AutoSolveReCaptcha">Auto-solve reCAPTCHA</Toggle>
</PlatformBase>
