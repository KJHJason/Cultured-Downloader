<script lang="ts">
    import { onMount } from "svelte";
    import { Tabs, TabItem } from "flowbite-svelte";
    import { UserCircleSolid, DownloadSolid, InfoCircleSolid, AdjustmentsVerticalSolid } from "flowbite-svelte-icons";
    import General from "./settings/General.svelte";

    export let username: string;
    export let handleActionChange: (event: CustomEvent<string>) => void;

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
                General
            </div>
            <General username={username} on:changeUsername={handleActionChange} />
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <DownloadSolid size="sm" />
                Preferences
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Preferences:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <AdjustmentsVerticalSolid size="sm" />
                Platforms
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Settings:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
        <TabItem class="text-main">
            <div slot="title" class="flex items-center gap-2">
                <InfoCircleSolid size="sm" />
                Program Info
            </div>
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Users:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
    </Tabs>
</div>
