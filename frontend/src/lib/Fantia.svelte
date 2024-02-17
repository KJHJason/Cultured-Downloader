<script lang="ts">
    import PlatformBase from "./PlatformBase.svelte";
    import { Checkbox, Helper, Hr } from "flowbite-svelte";

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

    const settingConfigFn = async (): Promise<void> => {

    };

    const checkUrlHasPageNumFilter = (inputUrl: string): boolean => {
        return inputUrl.startsWith("https://fantia.jp/fanclubs/");
    };
</script>

<PlatformBase 
    platformName="Fantia" 
    inputPlaceholder={"https://fantia.jp/posts/2239524\nhttps://fantia.jp/fanclubs/5744"} 
    urlValidationFn={urlValidationFn}
    settingConfigFn={settingConfigFn}
    checkUrlHasPageNumFilter={checkUrlHasPageNumFilter}
>
    <Checkbox name="dl-gdrive-links" id="dl-gdrive-links">GDrive Links</Checkbox>
    <Checkbox name="detect-other-links" id="detect-other-links">Detect Other URL(s) like MEGA</Checkbox>
    <Checkbox name="auto-solve-recaptcha" id="auto-solve-recaptcha">Auto-solve reCAPTCHA</Checkbox>
</PlatformBase>
