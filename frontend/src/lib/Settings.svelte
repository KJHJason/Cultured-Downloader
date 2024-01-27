<script>
    import { Input, Label, Tabs, TabItem, Helper, Fileupload } from "flowbite-svelte";
</script>

<div class="container mx-auto">
    <Tabs style="underline">
        <TabItem class="text-main" open title="Profile">
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
        <TabItem class="text-main" title="Preferences">
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Preferences:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
        <TabItem class="text-main" title="Settings">
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Settings:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
        <TabItem class="text-main" title="Users">
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Users:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
        <TabItem disabled>
            <span slot="title" class="text-gray-400 dark:text-gray-500">Disabled</span>
            <p class="text-sm text-gray-500 dark:text-gray-400">
            <b>Disabled:</b>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
        </TabItem>
    </Tabs>
</div>
