<!-- <script lang="ts">
    import { Textarea, Label, Card, Hr  } from "flowbite-svelte";

    const placeholderPrefix = "Examples of Fantia URLs:\n";
    const inputPlaceholder = placeholderPrefix + "https://fantia.jp/posts/2239524\nhttps://fantia.jp/fanclubs/5744";
</script>

<div class="container mx-auto">
    <Card class="max-w-full" size="xl">
        <h3>Input Fantia URLs</h3>
        <Hr />
        <Textarea id="fantiaUrls" rows="8" placeholder="{inputPlaceholder}" />
    </Card>

    <Card class="mt-4 max-w-full" size="xl">
        <h3>Fantia Settings</h3>
        <Hr />
    </Card>
</div> -->

<script lang="ts">
    import PlatformBase from "./PlatformBase.svelte";
    import { Checkbox, Helper, Hr } from "flowbite-svelte";

    const urlValidationFn = (textareaInput: string): boolean => {
        const urls = textareaInput.split("\n");
        const urlRegex = /https:\/\/fantia.jp\/(posts|fanclubs)\/\d+/;
        for (const url of urls) {
            if (!urlRegex.test(url)) {
                return false;
            }
        }
        return true;
    };

    const settingConfigFn = async (): Promise<void> => {

    };
</script>

<PlatformBase 
    platformName="Fantia" 
    inputPlaceholder={"https://fantia.jp/posts/2239524\nhttps://fantia.jp/fanclubs/5744"} 
    urlValidationFn={urlValidationFn}
    settingConfigFn={settingConfigFn}
>
    <Helper>This settings is for the current download inputs. However, you can save it globally by clicking "Save Settings" Button below!</Helper>
    <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 ">
        <Checkbox name="dl-post-thumbnail" id="dl-post-thumbnail">Post Thumbnail</Checkbox>
        <Checkbox name="dl-post-images" id="dl-post-images">Post Images</Checkbox>
        <Checkbox name="dl-post-attachments" id="dl-post-attachments">Post Attachments</Checkbox>
        <Checkbox name="dl-gdrive-links" id="dl-gdrive-links">GDrive Links</Checkbox>
        <Checkbox name="detect-other-links" id="detect-other-links">Detect Other URL(s) like MEGA</Checkbox>
    </div>
    <Hr />
    <div class="text-right">
        <button class="btn btn-success">Save Settings Globally</button>
    </div>
</PlatformBase>
