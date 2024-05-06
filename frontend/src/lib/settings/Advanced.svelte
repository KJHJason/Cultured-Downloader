<script lang="ts">
    import { Input, ButtonGroup, Label } from "flowbite-svelte";
    import ButtonGroupBtn from "../common/ButtonGroupBtn.svelte";
    import { SelectDlDirPath, SetDlDirPath, GetDownloadDir, GetUserAgent, SetUserAgent } from "../../scripts/wailsjs/go/app/App";
    import { onMount } from "svelte";
    import { swal } from "../../scripts/constants";

    let savedUserAgent: string;
    let savedDownloadLoc: string;
    let dlLocationInp: HTMLInputElement;
    const SelectDownloadDir = async () => {
        try {
            await SelectDlDirPath();
        } catch (e) {
            if (e === "no directory selected") {
                return;
            }
            throw e;
        }

        swal.fire({
            title: "Success",
            text: "Download location set successfully",
            icon: "success",
        });
        if (dlLocationInp) {
            savedDownloadLoc = await GetDownloadDir();
            dlLocationInp.value = savedDownloadLoc;
        }
    }

    onMount(async () => {
        dlLocationInp = document.getElementById("downloadLocation") as HTMLInputElement;
        savedDownloadLoc = await GetDownloadDir();
        dlLocationInp.value = savedDownloadLoc;

        const userAgentInp = document.getElementById("userAgent") as HTMLInputElement;
        savedUserAgent = await GetUserAgent();
        userAgentInp.value = savedUserAgent;

        const form = document.getElementById("advanced-form") as HTMLFormElement;
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const downloadLocation = dlLocationInp.value;
            const userAgent = userAgentInp.value;

            if (userAgent !== savedUserAgent) {
                await SetUserAgent(userAgent);
                savedUserAgent = userAgent;
            }

            if (downloadLocation !== savedDownloadLoc) {
                await SetDlDirPath(downloadLocation);
                savedDownloadLoc = downloadLocation;
            }
            swal.fire({
                title: "Success",
                text: "Settings saved successfully",
                icon: "success",
            });
        });
    });
</script>

<!-- <p class="text-sm text-gray-500 dark:text-gray-400">
<b>Advanced Settings:</b>
</p>

<ul>
    <li>User agents</li>
    <li>Download location</li>
    <li>GDrive Setup</li>
</ul> -->

<form class="grid grid-cols-1 md:grid-cols-1 gap-4" id="advanced-form">
    <div>
        <Label for="userAgent">User Agent (*DO NOT EDIT IF UNSURE):</Label>
        <Input class="mt-2" name="userAgent" id="userAgent" placeholder="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..." />
    </div>
    <div>
        <Label for="downloadLocation">Download Location:</Label>
        <ButtonGroup class="w-full">
            <Input class="mt-2" name="downloadLocation" id="downloadLocation" placeholder="C:\Users\Username\Downloads" />
            <ButtonGroupBtn elId="downloadLocation" clickFn={SelectDownloadDir}>Browse</ButtonGroupBtn>
        </ButtonGroup>
    </div>
</form>
