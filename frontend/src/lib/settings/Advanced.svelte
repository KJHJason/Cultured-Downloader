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
        UnsetGDriveJson,
        StartPixivOAuth,
        VerifyPixivOAuthCode,
        SetPixivOAuthRefreshToken,
        GetPixivRefreshToken,
        SelectFfmpegPath,
        SetFfmpegPath,
        GetFfmpegPath,
        ValidateGDriveOauth,
        StartGDriveOauth,
        CancelGDriveOauth,
        GetGDriveClientAndOauthToken,
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
    let savedFfmpegPath: string;
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

    const SelectFfmpegPathFn = async (): Promise<void> => {
        try {
            await SelectFfmpegPath();
        } catch (e) {
            if (e === "no file selected") {
                return;
            }
            throw e;
        }

        swal.fire({
            title: "Success",
            text: "FFmpeg location set successfully",
            icon: "success",
        });
    };

    const handleGdriveResponse = (val: string): void => {
        gdriveJsonText.classList.remove("hidden");
        savedGdriveJson = val;
    };

    const getGDriveClientAndOauthToken = async (): Promise<void> => {
        const oauthResponse = await GetGDriveClientAndOauthToken();
        const client = oauthResponse.ClientJson;
        const token = oauthResponse.TokenJson;
        if (client && token) {
            const gdriveContent = `Client Secret JSON: ${client}\n\nOAuth Token JSON: ${token}`;
            handleGdriveResponse(gdriveContent);
        }
    };

    const StartGDriveOauthProcess = async (oauthUrl: string): Promise<void> => {
        await StartGDriveOauth();
        BrowserOpenURL(oauthUrl);
        const result = await swal.fire({
            title: "Authentication Required for OAuth",
            text: `Please visit the recently opened tab in your default browser and authenticate yourself.`,
            icon: "info",
            showConfirmButton: true,
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            showLoaderOnConfirm: true,
            cancelButtonText: "Cancel",
            confirmButtonText: "Verify",
            preConfirm: async (): Promise<void> => {
                try {
                    await ValidateGDriveOauth();
                } catch (e) {
                    if (!e) {
                        CancelGDriveOauth();
                        throw new Error("An error occurred while trying to verify OAuth2 flow for Google Cloud Platform.");
                    }

                    const error = e.toString();
                    if (error === "oauth not finished") {
                        return swal.showValidationMessage("Authentication not finished yet. Please try again.");
                    }
                    swal.showValidationMessage(error);
                }
                return;
            },
        });

        if (result.isConfirmed) {
            swal.fire({
                icon: "success",
                title: "Authentication Success",
                text: "You have successfully authenticated yourself.",
            });
            await getGDriveClientAndOauthToken();
            return;
        }

        await CancelGDriveOauth();
        swal.fire({
            icon: "info",
            title: "Authentication Cancelled",
            text: "You have cancelled the authentication process.",
        });
    }

    const SelectGDriveServiceAcc = async (): Promise<void> => {
        try {
            await SelectGDriveServiceAccount();
        } catch (e) {
            if (!e) {
                throw new Error("An error occurred while trying to upload the JSON file for GDrive API.");
            }

            const error = e.toString();
            if (error === "no file selected") {
                return;
            }
            if (error.startsWith("authentication needed, ")) {
                const oauthUrl = error.split(", ")[1];
                StartGDriveOauthProcess(oauthUrl);
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
            text: "Google Cloud Platform credentials JSON file uploaded successfully",
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
        } else {
            getGDriveClientAndOauthToken();
        }

        const ffmpegLocationInp = document.getElementById("ffmpegLocation") as HTMLInputElement;
        savedFfmpegPath = await GetFfmpegPath();
        ffmpegLocationInp.value = savedFfmpegPath;

        gdriveJsonText.addEventListener("click", async () => {
            const result = await swal.fire({
                title: "Google Cloud Platform Credentials JSON",
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
                text: "Are you sure you want to delete the Google Cloud Platform credentials JSON file?",
                icon: "info",
                showCancelButton: true,
                confirmButtonText: "Yes",
            });
            if (deleteResult.isConfirmed) {
                await UnsetGDriveJson()
                savedGdriveJson = "";
                gdriveJsonText.classList.add("hidden");
                swal.fire({
                    title: "Success",
                    text: "Google Cloud Platform credentials JSON file deleted successfully",
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
            const ffmpegLocation = ffmpegLocationInp.value;

            if (userAgent && userAgent !== savedUserAgent) {
                await SetUserAgent(userAgent);
                savedUserAgent = userAgent;
            }

            if (downloadLocation !== savedDownloadLoc) {
                await SetDlDirPath(downloadLocation);
                savedDownloadLoc = downloadLocation;
            }

            if (savedFfmpegPath !== ffmpegLocation) {
                await SetFfmpegPath(ffmpegLocation);
                savedFfmpegPath = ffmpegLocation;
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
                <Label for="gdriveApiKey">{Translate("GCP Credentials:")}</Label>
                <button type="button" class="hidden btn-text-link text-xs font-normal ml-1" id="gdrive-json-text">
                    {Translate("View Uploaded JSON")}
                </button>
            </div>
            <ButtonGroup class="w-full">
                <PasswordToggle elClass="w-full" hideByDefault={true}>
                    <Input class="mt-2" name="gdriveApiKey" id="gdriveApiKey" placeholder="API Key: AIzaSyDanMyMjsRgQEeCynXiXZK_LdaZA40N0YM" />
                </PasswordToggle>
                <ButtonGroupBtn elId="browseApiJson" clickFn={SelectGDriveServiceAcc}>
                    <UploadSolid />
                </ButtonGroupBtn>
            </ButtonGroup>
            <Tooltip triggeredBy="#browseApiJson">{Translate("Upload Google Cloud Platform JSON file")}</Tooltip>
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
                *{Translate("If you're unsure what to do after clicking \"Start OAuth\", please refer to the guide below.")} 
            </Helper>
            <Helper>
                <button type="button" class="btn-link text-left" on:click={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/pixiv_oauth_guide.md")}>
                    https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/pixiv_oauth_guide.md
                </button>
            </Helper>
        </div>
        <div>
            <Label for="ffmpegLocation">{Translate("FFmpeg Location:")}</Label>
            <ButtonGroup class="w-full">
                <Input class="mt-2" name="ffmpegLocation" id="ffmpegLocation" placeholder="C:\ffmpeg\bin\ffmpeg.exe" required />
                <ButtonGroupBtn elId="browseFfmpegLocation" clickFn={SelectFfmpegPathFn}>{Translate("Browse")}</ButtonGroupBtn>
            </ButtonGroup>
            <Helper class="mt-2">
                *{Translate("This is used for Pixiv Ugoira downloads. If you're not downloading from Pixiv, you can ignore this. Otherwise you can install it from the link below.")}
            </Helper>
            <Helper>
                <button type="button" class="btn-link text-left" on:click={() => BrowserOpenURL("https://ffmpeg.org/download.html")}>
                    https://ffmpeg.org/download.html
                </button>
            </Helper>
        </div>
    </div>
    <div class="text-right">
        <button type="submit" class="mt-2 btn btn-success !me-0">
            {Translate("Save All")}
        </button>
    </div>
</form>
