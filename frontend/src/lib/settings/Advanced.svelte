<script lang="ts">
    import { BrowserOpenURL } from "../../scripts/wailsjs/runtime/runtime";
    import { Input, ButtonGroup, Label, Tooltip, Helper } from "flowbite-svelte";
    import ButtonGroupBtn from "../common/ButtonGroupBtn.svelte";
    import { 
        SelectDlDirPath,
        SetDlDirPath, 
        GetDownloadDir, 
        GetUserAgent, 
        SetUserAgent,
        GetGDriveServiceAccount, 
        SelectGDriveServiceAccount, 
        UnsetGDriveServiceAccount,
        StartPixivOAuth,
        VerifyPixivOAuthCode,
        SetPixivOAuthRefreshToken,
        GetPixivRefreshToken,
    } from "../../scripts/wailsjs/go/app/App";
    import { onMount } from "svelte";
    import { invertedSwal, swal } from "../../scripts/constants";
    import { UploadSolid } from "flowbite-svelte-icons";
    import { Translate } from "../../scripts/language";
    import PasswordToggle from "../common/PasswordToggle.svelte";

    let pixivRefreshToken: string;
    let savedUserAgent: string;
    let savedDownloadLoc: string;
    let savedGdriveJson: string;
    let gdriveJsonText: HTMLButtonElement;
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
    };

    const handleGdriveResponse = (val: string): void => {
        gdriveJsonText.classList.remove("hidden");
        savedGdriveJson = val;
    };

    const SelectGDriveServiceAcc = async (): Promise<void> => {
        try {
            await SelectGDriveServiceAccount();
        } catch (e) {
            if (e === "no file selected") {
                return;
            }
            throw e;
        }

        const savedGdriveJsonBytes = await GetGDriveServiceAccount();
        if (savedGdriveJsonBytes) {
            handleGdriveResponse(savedGdriveJsonBytes);
        }
        swal.fire({
            title: "Success",
            text: "Google Drive API JSON file uploaded successfully",
            icon: "success",
        });
    };

    const startPixivOauthProcess = async (): Promise<void> => {
        const url = await StartPixivOAuth();
        BrowserOpenURL(url);

        swal.fire({
            title: "Enter OAuth Code",
            input: "password",
            inputAttributes: {
                autocapitalize: "off",
                autocorrect: "off",
            },
            showCancelButton: true,
            confirmButtonText: "Submit",
            allowEscapeKey: false,
            allowOutsideClick: false,
            preConfirm: async (code: string): Promise<void> => {
                if (code === "") {
                    return swal.showValidationMessage("Code cannot be empty");
                }
                try {
                    await VerifyPixivOAuthCode(code);
                    swal.fire({
                        title: "Success",
                        text: "Pixiv OAuth code verified successfully and your Pixiv OAuth refresh token has been saved successfully.",
                        icon: "success",
                    });
                } catch (e) {
                    if (e) {
                        return swal.showValidationMessage(e.toString());
                    }
                }
            },
        })
    };

    onMount(async () => {
        dlLocationInp = document.getElementById("downloadLocation") as HTMLInputElement;
        savedDownloadLoc = await GetDownloadDir();
        dlLocationInp.value = savedDownloadLoc;

        const pixivOauthInp = document.getElementById("pixivOauth") as HTMLInputElement;
        pixivRefreshToken = await GetPixivRefreshToken();
        if (pixivRefreshToken) {
            pixivOauthInp.value = pixivRefreshToken;
        }

        const userAgentInp = document.getElementById("userAgent") as HTMLInputElement;
        const userAgentResp = await GetUserAgent();
        savedUserAgent = userAgentResp.UserAgent;
        if (userAgentResp.IsDefault) {
            userAgentInp.placeholder = savedUserAgent;
        } else {
            userAgentInp.value = savedUserAgent;
        }

        gdriveJsonText = document.getElementById("gdrive-json-text") as HTMLButtonElement;
        const savedGdriveJsonBytes = await GetGDriveServiceAccount();
        if (savedGdriveJsonBytes) {
            handleGdriveResponse(savedGdriveJsonBytes);
        }

        gdriveJsonText.addEventListener("click", async () => {
            const result = await swal.fire({
                title: "Google Drive API JSON",
                html: `<pre class="overflow-x-auto text-left"><code class="block text-sm font-mono">${savedGdriveJson}</code></pre>`,
                icon: "info",
                showDenyButton: true,
                denyButtonText: "Delete",
            });
            if (!result.isDenied) {
                return;
            }

            const deleteResult = await invertedSwal.fire({
                title: "Delete GDrive API JSON file?",
                text: "Are you sure you want to delete the Google Drive API JSON file?",
                icon: "info",
                showCancelButton: true,
                confirmButtonText: "Yes",
            });
            if (deleteResult.isConfirmed) {
                await UnsetGDriveServiceAccount()
                savedGdriveJson = "";
                gdriveJsonText.classList.add("hidden");
                swal.fire({
                    title: "Success",
                    text: "Google Drive API JSON file deleted successfully",
                    icon: "success",
                });
            }
        });

        const form = document.getElementById("advanced-form") as HTMLFormElement;
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const downloadLocation = dlLocationInp.value;
            const userAgent = userAgentInp.value;
            const pixivOauthCode = pixivOauthInp.value;

            if (userAgent && userAgent !== savedUserAgent) {
                await SetUserAgent(userAgent);
                savedUserAgent = userAgent;
            }

            if (downloadLocation !== savedDownloadLoc) {
                await SetDlDirPath(downloadLocation);
                savedDownloadLoc = downloadLocation;
            }

            if (pixivOauthCode) {
                await SetPixivOAuthRefreshToken(pixivOauthCode);
                pixivRefreshToken = await GetPixivRefreshToken();
                pixivOauthInp.value = pixivRefreshToken;
            }

            swal.fire({
                title: "Success",
                text: "Settings saved successfully",
                icon: "success",
            });
        });
    });
</script>

<form id="advanced-form">
    <div class="grid grid-cols-1 md:grid-cols-1 gap-y-6">
        <div>
            <Label for="userAgent">{Translate("User Agent:")}</Label>
            <Input class="my-2" name="userAgent" id="userAgent" placeholder="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..." />
            <Helper>*{Translate("Only edit this when you know what you're doing as you can be flagged as a bot with the wrong user agent!")}</Helper>
        </div>
        <div>
            <Label for="downloadLocation">{Translate("Download Location:")}</Label>
            <ButtonGroup class="w-full">
                <Input class="mt-2" name="downloadLocation" id="downloadLocation" placeholder="C:\Users\Username\Downloads" required />
                <ButtonGroupBtn elId="browseDownloadLocation" clickFn={SelectDownloadDir}>{Translate("Browse")}</ButtonGroupBtn>
            </ButtonGroup>
        </div>
        <div>
            <div class="flex">
                <Label for="gdriveApiKey">{Translate("GDrive Credentials:")}</Label>
                <button type="button" class="btn-link hidden" id="gdrive-json-text">
                    <Helper class="ml-1">{Translate("View Uploaded JSON")}</Helper>
                </button>
            </div>
            <ButtonGroup class="w-full">
                <PasswordToggle elClass="w-full" hideByDefault={true}>
                    <Input class="mt-2" name="gdriveApiKey" id="gdriveApiKey" placeholder="AIzaSyDanMyMjsRgQEeCynXiXZK_LdaZA40N0YM" />
                </PasswordToggle>
                <ButtonGroupBtn elId="browseApiJson" clickFn={SelectGDriveServiceAcc}>
                    <UploadSolid />
                </ButtonGroupBtn>
            </ButtonGroup>
            <Tooltip triggeredBy="#browseApiJson">{Translate("Upload Google Drive API JSON file")}</Tooltip>
        </div>
        <div>
            <Label for="pixivOauth">{Translate("Pixiv Mobile OAuth Refresh Token:")}</Label>
            <ButtonGroup class="w-full">
                <PasswordToggle elClass="w-full" hideByDefault={true}>
                    <Input class="mt-2" name="pixivOauth" id="pixivOauth" placeholder="zKyAG1RaKUgAK1AB-DEFaIodef12345aBcDeF3zQLcX" required />
                </PasswordToggle>
                <ButtonGroupBtn btnClass="w-[140px]" elId="startPixivOauthBtn" clickFn={startPixivOauthProcess}>
                    {Translate("Start OAuth")}
                </ButtonGroupBtn>
            </ButtonGroup>
            <Helper class="mt-2">
                *If you're unsure what to do after clicking "Start OAuth", please refer to this 
                <button type="button" class="btn-link" on:click={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/pixiv_oauth_guide.md")}>guide</button>.
            </Helper>
        </div>
    </div>
    <div class="text-right">
        <button type="submit" class="mt-2 btn btn-success !me-0">
            {Translate("Save All")}
        </button>
    </div>
</form>
