<script lang="ts">
    import { Input, Tooltip, ButtonGroup } from "flowbite-svelte";
    import { UploadCookieFile } from "../../scripts/wailsjs/go/app/App";
    import { UploadSolid } from "flowbite-svelte-icons";
</script>

<!-- 
1. Fantia Session
2. Pixiv Fanbox Session
3. Pixiv Session
4. Kemono Session

-->
<div class="grid grid-cols-1 gap-y-6">
    <div>
        <h4>Fantia</h4>
        <div>
            <ButtonGroup class="w-full">
                <Input 
                    class="mt-2" 
                    name="fantiaSessionInp" 
                    id="fantiaSessionInp" 
                    type="text"
                    placeholder="f6ec2f56f413b4c41e4eb95..."
                />
                <button on:click={() => UploadCookieFile("fantia")} id="fantia-session-upload" class="p-2 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 dark:border-gray-600 rounded-r-lg rounded-l-none mt-2">
                    <UploadSolid />
                </button>
                <Tooltip triggeredBy="#fantia-session-upload">Upload Netscape/Mozilla generated cookie .txt file</Tooltip>
            </ButtonGroup>
            
        </div>
    </div>
</div>
