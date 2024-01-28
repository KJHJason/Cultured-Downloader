<script>
    import { onMount } from "svelte";
    import { Input, Label, Tabs, TabItem, Helper, Fileupload } from "flowbite-svelte";
    import { UserCircleSolid, DownloadSolid, InfoCircleSolid, AdjustmentsVerticalSolid } from "flowbite-svelte-icons";

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
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="mx-auto">
                    <img class="rounded-full w-32 h-32 border-4 mt-2 border-gray-200" id="photo" src="https://avatars.githubusercontent.com/u/73630142?v=4" alt="test">
                </div>
                <div class="md:col-span-3 flex items-center">
                    <div class="w-full">
                        <Label for="profile-image" class="pb-2">Upload file</Label>
                        <Fileupload id="profile-image" class="mb-2" />
                        <Helper>SVG, PNG, JPG or GIF (MAX. 800x400px).</Helper>
                    </div>
                </div>
            </div>
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
                Settings
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
