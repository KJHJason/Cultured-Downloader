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
    import { invertedSwal, swal, pleaseWaitSwal } from "../../scripts/constants";
    import { UploadSolid } from "flowbite-svelte-icons";
    import { translate, translateText } from "../../scripts/language";
    import PasswordToggle from "../common/PasswordToggle.svelte";
    import Translate from "../common/Translate.svelte";

    let pixivRefreshToken: string;
    let savedUserAgent: string;
    let savedDownloadLoc: string;
    let savedGdriveJson: string;
    let savedFfmpegPath: string;
    let gdriveJsonText: HTMLButtonElement;
    let dlLocationInp: HTMLInputElement;

    let pixivOauthInp: HTMLInputElement;

    let successText: string;
    let submitText: string;
    let downloadLocSuccessText: string;
    let ffmpegLocSuccessText: string;
    let googleClientJsonText: string;
    let googleOauthJsonText: string;
    let googleOauthAuthTitle: string;
    let googleOauthAuthMsg: string;
    let cancelText: string;
    let verifyText: string;
    let oauthVerifyErrText: string;
    let oauthNotFinishedText: string;
    let authenticatedText: string;
    let authenticatedMsg: string;
    let authenticationCancelledText: string;
    let authenticationCancelledMsg: string;
    let uploadFailedText: string;
    let uploadedFileText: string;
    let pixivOauthStartTitle: string;
    let pixivOauthCodeEmptyText: string;
    let pixivOauthVerifiedText: string;

    onMount(async() => {
        successText = await translateText("Success");
        submitText = await translateText("advanced_submit", "", "Submit");

        downloadLocSuccessText = await translateText("Download location set successfully");

        ffmpegLocSuccessText = await translateText("FFmpeg location set successfully");

        googleClientJsonText = await translateText("Client Secret JSON:");
        googleOauthJsonText = await translateText("OAuth Token JSON:");

        googleOauthAuthTitle = await translateText("Authentication Required for OAuth");
        googleOauthAuthMsg = await translateText("Please visit the recently opened tab in your default browser and authenticate yourself.");

        cancelText = await translateText("Cancel");
        verifyText = await translateText("Verify");
        oauthVerifyErrText = await translateText("An error occurred while trying to verify OAuth2 flow for Google Cloud Platform.");
        oauthNotFinishedText = await translateText("Authentication not finished yet. Please try again.");

        authenticatedText = await translateText("Authentication Success");
        authenticatedMsg = await translateText("You have successfully authenticated yourself.");

        authenticationCancelledText = await translateText("Authentication Cancelled");
        authenticationCancelledMsg = await translateText("You have cancelled the authentication process.");

        uploadFailedText = await translateText("An error occurred while trying to upload the JSON file for GDrive API.");
        uploadedFileText = await translateText("Google Cloud Platform credentials JSON file uploaded successfully");

        pixivOauthStartTitle = await translateText("Enter Pixiv OAuth Code");
        pixivOauthCodeEmptyText = await translateText("Pixiv code cannot be empty");
        pixivOauthVerifiedText = await translateText("Pixiv OAuth code verified successfully and your Pixiv OAuth refresh token has been saved successfully.");
    });

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
            title: successText,
            text: downloadLocSuccessText,
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
            title: successText,
            text: ffmpegLocSuccessText,
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
            const gdriveContent = `${googleClientJsonText} ${client}\n\n${googleOauthJsonText} ${token}`;
            handleGdriveResponse(gdriveContent);
        }
    };

    const StartGDriveOauthProcess = async (oauthUrl: string): Promise<void> => {
        await StartGDriveOauth();
        BrowserOpenURL(oauthUrl);
        const result = await swal.fire({
            title: googleOauthAuthTitle,
            text: googleOauthAuthMsg,
            icon: "info",
            showConfirmButton: true,
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            showLoaderOnConfirm: true,
            cancelButtonText: cancelText,
            confirmButtonText: verifyText,
            preConfirm: async (): Promise<void> => {
                try {
                    await ValidateGDriveOauth();
                } catch (e) {
                    if (!e) {
                        CancelGDriveOauth();
                        throw new Error(oauthVerifyErrText);
                    }

                    const error = e.toString();
                    if (error === "oauth not finished") {
                        BrowserOpenURL(oauthUrl);
                        return swal.showValidationMessage(oauthNotFinishedText);
                    }
                    swal.showValidationMessage(error);
                }
                return;
            },
        });

        if (result.isConfirmed) {
            swal.fire({
                icon: "success",
                title: authenticatedText,
                text: authenticatedMsg,
            });
            await getGDriveClientAndOauthToken();
            return;
        }

        await CancelGDriveOauth();
        swal.fire({
            icon: "info",
            title: authenticationCancelledText,
            text: authenticationCancelledMsg,
        });
    }

    const SelectGDriveServiceAcc = async (): Promise<void> => {
        try {
            await SelectGDriveServiceAccount();
        } catch (e) {
            if (!e) {
                throw new Error(uploadFailedText);
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
            title: successText,
            text: uploadedFileText,
            icon: "success",
        });
    };

    const startPixivOauthProcess = async (): Promise<void> => {
        const url = await StartPixivOAuth();
        BrowserOpenURL(url);

        swal.fire({
            title: pixivOauthStartTitle,
            input: "password",
            inputAttributes: {
                autocapitalize: "off",
                autocorrect: "off",
            },
            showCancelButton: true,
            cancelButtonText: cancelText,
            confirmButtonText: submitText,
            allowEscapeKey: false,
            allowOutsideClick: false,
            preConfirm: async (code: string): Promise<void> => {
                if (code === "") {
                    return swal.showValidationMessage(pixivOauthCodeEmptyText);
                }
                try {
                    await VerifyPixivOAuthCode(code);
                    pixivRefreshToken = await GetPixivRefreshToken();
                    pixivOauthInp.value = pixivRefreshToken;
                    swal.fire({
                        title: successText,
                        text: pixivOauthVerifiedText,
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

    let form: HTMLFormElement | null = $state(null);
    onMount(async () => {
        dlLocationInp = document.getElementById("downloadLocation") as HTMLInputElement;
        savedDownloadLoc = await GetDownloadDir();
        dlLocationInp.value = savedDownloadLoc;

        pixivOauthInp = document.getElementById("pixivOauth") as HTMLInputElement;
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

        const gdriveJsonTextTitle = await translateText("Google Cloud Platform Credentials JSON");
        const deleteText = await translateText("Delete");
        const gdriveDeleteJsonTitle = await translateText("Delete Google Cloud Platform credentials JSON file?");
        const gdriveDeleteJsonMsg = await translateText("Are you sure you want to delete the Google Cloud Platform credentials JSON file?");
        const yesText = await translateText("Yes");
        const deletedGdriveMsg = await translateText("Google Cloud Platform credentials JSON file deleted successfully");

        gdriveJsonText.addEventListener("click", async () => {
            const result = await swal.fire({
                title: gdriveJsonTextTitle,
                html: `<pre class="overflow-x-auto text-left"><code class="block text-sm font-mono">${savedGdriveJson}</code></pre>`,
                icon: "info",
                showDenyButton: true,
                denyButtonText: deleteText,
            });
            if (!result.isDenied) {
                return;
            }

            const deleteResult = await invertedSwal.fire({
                title: gdriveDeleteJsonTitle,
                text: gdriveDeleteJsonMsg,
                icon: "info",
                showCancelButton: true,
                confirmButtonText: yesText,
                cancelButtonText: cancelText,
            });
            if (deleteResult.isConfirmed) {
                await UnsetGDriveJson()
                savedGdriveJson = "";
                gdriveJsonText.classList.add("hidden");
                swal.fire({
                    title: "Success",
                    text: deletedGdriveMsg,
                    icon: "success",
                });
            }
        });

        const savingText = await translateText("Saving...");
        const pleaseWaitText = await translateText("Please wait a moment.");
        const settingSavedText = await translateText("Settings saved successfully");

        if (form === null) {
            throw new Error("Advanced settings form not initialised yet");
        }
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            pleaseWaitSwal.fire({
                title: savingText,
                text: pleaseWaitText,
            })

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
                title: successText,
                text: settingSavedText,
                icon: "success",
            });
        });
    });

    let browseApiJsonText = $state("");
    
    onMount(async () => {
        browseApiJsonText = await translateText("Upload Google Cloud Platform JSON file");
    });
</script>

<form bind:this={form}>
    <div class="grid grid-cols-1 md:grid-cols-1 gap-y-6">
        <div>
            <Label for="userAgent">
                <Translate text="User Agent:" />
            </Label>
            <Input class="my-2" name="userAgent" id="userAgent" placeholder="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..." />
            <Helper>*<Translate text="Only edit this when you know what you're doing as you can be flagged as a bot with the wrong user agent!" /></Helper>
        </div>
        <div>
            <Label for="downloadLocation">
                <Translate text="Download Location:" />
            </Label>
            <ButtonGroup class="w-full">
                <Input class="mt-2" name="downloadLocation" id="downloadLocation" placeholder="C:\Users\Username\Downloads" required />
                <ButtonGroupBtn elId="browseDownloadLocation" clickFn={SelectDownloadDir}>
                    <Translate spanClass="whitespace-nowrap" text="Browse" />
                </ButtonGroupBtn>
            </ButtonGroup>
        </div>
        <div>
            <div class="flex">
                <Label for="gdriveApiKey">
                    <Translate text="GDrive Credentials:" />
                </Label>
                <button type="button" class="hidden btn-text-link text-xs font-normal ml-1" id="gdrive-json-text">
                    {translate("View Uploaded JSON", "gdrive-json-text")}
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
            <Helper class="mt-2">
                *<Translate text="If you're unsure how to obtain the relevant API key or credentials, please refer to the guide below." />
            </Helper>
            <Helper>
                <button type="button" class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/gcp_setup_guide.md")}>
                    https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/gcp_setup_guide.md
                </button>
            </Helper>
            <Tooltip triggeredBy="#browseApiJson">{browseApiJsonText}</Tooltip>
        </div>
        <div>
            <Label for="pixivOauth">
                <Translate text="Pixiv Mobile OAuth Refresh Token:" />
            </Label>
            <ButtonGroup class="w-full">
                <PasswordToggle elClass="w-full" hideByDefault={true}>
                    <Input class="mt-2" name="pixivOauth" id="pixivOauth" placeholder="zKyAG1RaKUgAK1AB-DEFaIodef12345aBcDeF3zQLcX" required />
                </PasswordToggle>
                <ButtonGroupBtn btnClass="whitespace-nowrap" elId="startPixivOauthBtn" clickFn={startPixivOauthProcess}>
                    {translate("Start OAuth", "startPixivOauthBtn")}
                </ButtonGroupBtn>
            </ButtonGroup>
            <Helper class="mt-2">
                *<Translate text={`If you're unsure what to do after clicking "Start OAuth", please refer to the guide below.`} />
            </Helper>
            <Helper>
                <button type="button" class="btn-link text-left" onclick={() => BrowserOpenURL("https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/pixiv_oauth_guide.md")}>
                    https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/pixiv_oauth_guide.md
                </button>
            </Helper>
        </div>
        <div>
            <Label for="ffmpegLocation">
                <Translate text="FFmpeg Location:" />
            </Label>
            <ButtonGroup class="w-full">
                <Input class="mt-2" name="ffmpegLocation" id="ffmpegLocation" placeholder="C:\ffmpeg\bin\ffmpeg.exe" required />
                <ButtonGroupBtn btnClass="whitespace-nowrap" elId="browseFfmpegLocation" clickFn={SelectFfmpegPathFn}>
                    {translate("Browse", "browseFfmpegLocation")}
                </ButtonGroupBtn>
            </ButtonGroup>
            <Helper class="mt-2">
                *<Translate text="This is used for Pixiv Ugoira downloads. If you're not downloading from Pixiv, you can ignore this. Otherwise you can install it from the link below." />
            </Helper>
            <Helper>
                <button type="button" class="btn-link text-left" onclick={() => BrowserOpenURL("https://ffmpeg.org/download.html")}>
                    https://ffmpeg.org/download.html
                </button>
            </Helper>
        </div>
    </div>
    <div class="text-right">
        <button type="submit" class="mt-2 btn btn-success !me-0">
            <Translate text="Save All" />
        </button>
    </div>
</form>
