<script lang="ts">
    import { onMount } from "svelte";
    import { Tabs, TabItem } from "flowbite-svelte";
    import { UserCircleSolid, DownloadSolid, InfoCircleSolid, AdjustmentsVerticalSolid, UserSettingsSolid } from "flowbite-svelte-icons";
    import General from "./settings/General.svelte";
    import Preferences from "./settings/Preferences.svelte";
    import Sessions from "./settings/Sessions.svelte";
    import Advanced from "./settings/Advanced.svelte";
    import ProgramInfo from "./settings/ProgramInfo.svelte";
    import type { Writable } from "svelte/store";
    import Translate from "./common/Translate.svelte";

    export let username: Writable<string>;
    export let language: Writable<string>;
    export let lastSavedUpdateStr: Record<string, string>;

    const changeDefaultDividerColour = () => {
        const settingsContent = document.getElementById("settingsContent");

        // Go to the second div child element within the settingsContent div
        const divider =  settingsContent?.children[1];
        if (divider) {
            divider.classList.remove("dark:bg-gray-700")
            divider.classList.add("dark:bg-gray-500");
        }
    };

    onMount(() => {
        changeDefaultDividerColour();
    });
</script>

<div class="container mx-auto" id="settingsContent">
    <Tabs style="underline">
        <TabItem class="text-main" open>
            <div slot="title" class="flex items-center gap-2">
                <UserCircleSolid size="sm" />
                <Translate text="General" {language} />
            </div>
            <General {username} {language} />
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <DownloadSolid size="sm" />
                <Translate text="Preferences" {language} />
            </div>
            <Preferences />
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <UserSettingsSolid size="sm" />
                <Translate text="Sessions" {language} />
            </div>
            <Sessions />
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <AdjustmentsVerticalSolid size="sm" />
                <Translate text="Advanced" {language} />
            </div>
            <Advanced />
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <InfoCircleSolid size="sm" />
                <Translate text="Program Info" {language} />
            </div>
            <ProgramInfo bind:lastSavedUpdateStr />
        </TabItem>
    </Tabs>
</div>
