<script lang="ts">
    import { onMount } from "svelte";
    import { Textarea, Helper, Card, Hr, Spinner } from "flowbite-svelte";
    import { actions, swal, pleaseWaitSwal } from "../scripts/constants";
    import { ArrowLeftOutline } from "flowbite-svelte-icons";
    import PixivSettings from "./settings/PixivSettings.svelte";
    import GeneralSettings from "./settings/GeneralSettings.svelte";
    import MergedSettings from "./settings/MergedSettings.svelte";
    import { GetPreferences } from "../scripts/wailsjs/go/app/App";
    import type { app } from "../scripts/wailsjs/go/models";
    import Translate from "./common/Translate.svelte";
    import { translateText } from "../scripts/language";

    let pixivArtworkType: number;
    let pixivRating: number;
    let pixivSearchMode: number;
    let pixivAiSearchMode: number;
    let pixivSortOrder: number;
    let pixivUgoiraFormat: number;

    let translatedPageNoPlaceholder: string;

    export let platformTitle: string = "";
    export let platformName: string;
    export let inputPlaceholder: string;
    export let urlValidationFn: (urls: string | string[]) => Promise<boolean>;
    export let checkUrlHasPageNumFilter: (inputUrl: string) => boolean;
    export let addToQueueFn: (inputs: string[], downloadSettings: app.Preferences) => Promise<void>;

    if (platformTitle === "") {
        platformTitle = platformName;
    }

    const GetPageNoInputs = (url: string): HTMLInputElement => {
        const input = document.createElement("input");
        input.type = "text"; // e.g. 1-2

        const inputClass = "bg-gray-50 border text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500";
        input.classList.add(...inputClass.split(" "));
        input.name = url;
        input.placeholder = translatedPageNoPlaceholder;
        return input;
    };

    const GetPageNoInputLabel = (url: string): HTMLLabelElement => {
        const label = document.createElement("label");
        const labelClass = "block mb-2 text-sm font-medium text-gray-900 dark:text-white";
        label.classList.add(...labelClass.split(" "));
        label.textContent = url + ":";
        return label;
    };

    let inputExampleText = "";
    $: hasPageNoFilter = false;
    const divId = `${platformName}-base`;
    onMount(async () => {
        translatedPageNoPlaceholder = await translateText("e.g. \"1\" for page 1 or \"1-2\" for pages 1 to 2");

        const divEl = document.getElementById(divId) as HTMLDivElement;
        const textareaEl = divEl.querySelector("textarea") as HTMLTextAreaElement;
        const helperEl = document.getElementById("url-helper") as HTMLParagraphElement;
        const pageNoDivEl = document.getElementById("page-no") as HTMLDivElement;
        const pageNoInputsDivEl = document.getElementById("page-no-inputs") as HTMLDivElement;
        const pageNoFilterHelper = document.getElementById("page-no-filter-helper") as HTMLParagraphElement;
        pageNoFilterHelper.classList.add("hidden");

        inputExampleText = await translateText("Input example:");
        const inputErrInvalidUrls = await translateText("Input Error: Invalid URL(s)!");
        const invalidUrls = await translateText("Invalid URL(s)!");
        const unknownInputError = await translateText("Unknown input error!");
        const inputErrNoUrl = await translateText("Input Error: No URL(s)!");
        const inputErr = await translateText("Input Error");
        const invalidPageNumFilterFmt = await translateText("Invalid Page Number Filter Format!");
        const addingToQueue = await translateText("Adding to Queue...");
        const addedToQueue = await translateText("Added to Queue!");
        const queuePleaseWait = await translateText("Please wait while the URL(s) are being processed and added to the download queue!");
        const urlAddedToQueue = await translateText("The URL(s) have been added to the download queue!");
        const loginFirst = await translateText(". Please login first!");

        const initialisePageNoValidations = (): void => {
            pageNoInputsDivEl.querySelectorAll("input").forEach((inputEl) => {
                inputEl.addEventListener("input", () => {
                    const input = inputEl.value;
                    if (input === "") {
                        pageNoFilterHelper.classList.add("hidden");
                        inputEl.classList.remove("!border-red-500");
                        return;
                    } 

                    const inputRegex = /^\d+(?:-\d+)?$/;
                    if (inputRegex.test(input)) {
                        pageNoFilterHelper.classList.add("hidden");
                        inputEl.classList.remove("!border-red-500");
                    } else {
                        pageNoFilterHelper.classList.remove("hidden");
                        inputEl.classList.add("!border-red-500");
                    }
                });
            })
        };

        const resetForm = (): void => {
            textareaEl.value = "";
            textareaEl.classList.remove("!border-red-500");
            helperEl.textContent = "";

            pageNoInputsDivEl.innerHTML = "";
            pageNoDivEl.classList.add("hidden");
            hasPageNoFilter = false;
        };
        textareaEl.addEventListener("input", async () => {
            const textareaInput = textareaEl.value;
            pageNoFilterHelper.classList.add("hidden");
            if (!textareaInput) {
                resetForm();
                return;
            }

            const urls = textareaInput.split("\n");
            const uniqueUrls = Array.from(new Set(urls));
            textareaEl.value = uniqueUrls.join("\n");

            hasPageNoFilter = false;
            const existsInUrls = new Set<string>();
            for (const url of uniqueUrls) {
                if (checkUrlHasPageNumFilter(url)) {
                    if (!hasPageNoFilter) {
                        hasPageNoFilter = true;
                    }

                    existsInUrls.add(url);
                    const duplicateInputEl = pageNoInputsDivEl.querySelector(`input[name="${url}"]`);
                    if (duplicateInputEl) {
                        continue;
                    }

                    const label = GetPageNoInputLabel(url);
                    const input = GetPageNoInputs(url);
                    pageNoInputsDivEl.appendChild(label);
                    pageNoInputsDivEl.appendChild(input);
                }
            }

            // Remove inputs that are not in the textarea 
            // (for better UX instead of just resetting the HTML content of the div)
            const allInputs = pageNoInputsDivEl.querySelectorAll("input");
            for (const inputEl of allInputs) {
                const url = inputEl.name;
                if (!existsInUrls.has(url)) {
                    pageNoInputsDivEl.removeChild(inputEl.previousElementSibling as HTMLLabelElement);
                    pageNoInputsDivEl.removeChild(inputEl);
                }
            }

            if (hasPageNoFilter) {
                initialisePageNoValidations();
            }

            const isValid = await urlValidationFn(uniqueUrls);
            if (isValid) {
                helperEl.textContent = "";
                textareaEl.classList.remove("!border-red-500");
            } else {
                helperEl.textContent = inputErrInvalidUrls;
                textareaEl.classList.add("!border-red-500");
            }
        });

        const settingsCard = document.getElementById("settings-card") as HTMLDivElement;
        const getDownloadSettingsFromForm = (): app.Preferences => {
            const checkboxes = settingsCard.querySelectorAll("input[type=checkbox]") as NodeListOf<HTMLInputElement>;
            const inputs = settingsCard.querySelectorAll("input") as NodeListOf<HTMLInputElement>;
            const downloadPreferences: app.Preferences = {
                DlPostThumbnail: false,
                DlPostImages: false,
                DlPostAttachments: false,
                OverwriteFiles: false,
                DlGDrive: false,
                DetectOtherLinks: false,
                UseCacheDb: false,
                OrganisePostImages: false,
                ArtworkType: pixivArtworkType,
                DeleteUgoiraZip: false,
                RatingMode: pixivRating,
                SearchMode: pixivSearchMode,
                AiSearchMode: pixivAiSearchMode,
                SortOrder: pixivSortOrder,
                UgoiraOutputFormat: pixivUgoiraFormat,
                UgoiraQuality: 10,
            };

            for (const checkbox of checkboxes) {
                const key = checkbox.name as keyof app.Preferences;
                downloadPreferences[key] = checkbox.checked as never;
            }
            for (const input of inputs) {
                if (input.type === "checkbox") {
                    continue;
                }

                const key = input.name as keyof app.Preferences;
                if (input.type === "number") {
                    downloadPreferences[key] = parseInt(input.value) as never;
                } else {
                    throw new Error(unknownInputError);
                }
            }
            return downloadPreferences;
        };

        const addToQueueForm = document.getElementById("add-to-queue-form") as HTMLFormElement;
        addToQueueForm.addEventListener("submit", async (e: Event): Promise<void> => {
            e.preventDefault();

            const textareaInput = textareaEl.value;
            if (textareaInput === "") {
                helperEl.textContent = inputErrNoUrl;
                swal.fire({
                    title: inputErr,
                    text: inputErrNoUrl,
                    icon: "error",
                });
                return;
            }

            const pageNoFilterIsValid = pageNoFilterHelper.classList.contains("hidden");
            if (!pageNoFilterIsValid) {
                swal.fire({
                    title: inputErr,
                    text: invalidPageNumFilterFmt,
                    icon: "error",
                });
                return;
            }

            const inputs = textareaInput.split("\n");
            const downloadPreferences = getDownloadSettingsFromForm();
            for (let i = 0; i < inputs.length; i++) {
                const input = inputs[i];
                const pageNoInput = pageNoInputsDivEl.querySelector(`input[name="${input}"]`) as HTMLInputElement;
                if (pageNoInput && pageNoInput.value !== "") {
                    inputs[i] += `;${pageNoInput.value}`;
                }
            }

            const isValid = await urlValidationFn(inputs);
            if (!isValid) {
                helperEl.textContent = inputErrInvalidUrls;
                swal.fire({
                    title: inputErr,
                    text: invalidUrls,
                    icon: "error",
                });
                return;
            }

            pleaseWaitSwal.fire({
                title: addingToQueue,
                text: queuePleaseWait,
            })
            try {
                await addToQueueFn(inputs, downloadPreferences);
                swal.fire({
                    timer: 2000,
                    title: addedToQueue,
                    text: urlAddedToQueue,
                    icon: "success",
                });
                resetForm();
            } catch (e) {
                if (e && e.toString().startsWith("no cookies found for")) {
                    swal.fire({
                        title: inputErr,
                        text: e + loginFirst,
                        icon: "error",
                    });
                    return;
                }
                throw e;
            }
        });
    });
</script>

<div class="container mx-auto" id={divId}>
    <form id="add-to-queue-form">
        <Card class="max-w-full" size="xl">
            <h4 class="capitalize">{platformTitle} <Translate text="Inputs" /></h4>
            <Hr />
            <Textarea 
                name="inputs"
                rows={6}
                placeholder={inputExampleText + "\n" + inputPlaceholder}
            />
            <div class="mt-2 text-right">
                <Helper id="url-helper" color="red" />
                <button type="submit" class="mt-2 btn btn-success" id="add-to-queue-btn">
                    <div class="flex text-main">
                        <ArrowLeftOutline class="" />
                        <Translate text="Add to queue!" />
                    </div>
                </button>
            </div>
        </Card>

        <Card class="mt-2 max-w-full max-h-[600px] overflow-y-auto {hasPageNoFilter ? "" : "hidden"}" id="page-no" size="xl">
            <h4><Translate text="Page Numbers Filter" /></h4>
            <Hr />
            <Helper>
                <Translate text="Note that this is OPTIONAL as you can leave this EMPTY to download all pages!" />
            </Helper>
            <div class="mt-4 space-y-4" id="page-no-inputs"></div>
            <div class="mt-2 text-right">
                <Helper color="red" id="page-no-filter-helper"><Translate text="Invalid Filter Format!" /></Helper>
            </div>
        </Card>
    </form>

    <Card class="mt-2 max-w-full" size="xl" id="settings-card">
        <h4><Translate text="Download Settings" /></h4>
        <Hr />
        {#await GetPreferences()}
            <div class="flex">
                <Spinner color="blue" /> <p class="ms-3"><Translate text="Loading form.." /></p>
            </div>
        {:then preferences}
            {@const isPixiv = platformName === actions.Pixiv}
            <Helper>
                <Translate text={`This settings is for the current download inputs. However, you can save it globally by clicking "Save Settings" Button below!`} />
            </Helper>
            <GeneralSettings promptSuccess={false} preferences={preferences} showDlGDriveInp={!isPixiv} showOrganisePostImagesInp={platformName === actions.Fantia} />
            {#if isPixiv}
                <Hr />
                <PixivSettings
                    promptSuccess={false}
                    preferences={preferences}
                    bind:pixivArtworkType
                    bind:pixivRating
                    bind:pixivSearchMode
                    bind:pixivAiSearchMode
                    bind:pixivSortOrder
                    bind:pixivUgoiraFormat
                />
            {/if}
            <Hr />
            <MergedSettings btnString="Save Settings Globally" />
        {/await}
    </Card>
</div>
