<script lang="ts">
    import { onMount } from "svelte";
    import { Textarea, Helper, Card, Hr, Spinner } from "flowbite-svelte";
    import { actions, swal } from "../scripts/constants";
    import { ArrowLeftOutline } from "flowbite-svelte-icons";
    import PixivSettings from "./settings/PixivSettings.svelte";
    import GeneralSettings from "./settings/GeneralSettings.svelte";
    import MergedSettings from "./settings/MergedSettings.svelte";
    import { GetPreferences } from "../scripts/wailsjs/go/app/App";

    let pixivArtworkType: number;
    let pixivRating: number;
    let pixivSearchMode: number;
    let pixivAiSearchMode: number;
    let pixivSortOrder: number;
    let pixivUgoiraFormat: number;

    export let platformTitle: string = "";
    export let platformName: string;
    export let inputPlaceholder: string;
    export let urlValidationFn: (urls: string | string[]) => Promise<boolean>;
    export let checkUrlHasPageNumFilter: (inputUrl: string) => boolean;
    export let addToQueueFn: (inputs: string[], downloadSettings: Record<string, any>) => Promise<void>;

    if (platformTitle === "") {
        platformTitle = platformName;
    }

    const GetPageNoInputs = (url: string): HTMLInputElement => {
        const input = document.createElement("input");
        input.type = "text"; // e.g. 1-2

        const inputClass = "bg-gray-50 border text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500";
        input.classList.add(...inputClass.split(" "));
        input.name = url;
        input.placeholder = "e.g. \"1\" for page 1 or \"1-2\" for pages 1 to 2";
        return input;
    };

    const GetPageNoInputLabel = (url: string): HTMLLabelElement => {
        const label = document.createElement("label");
        const labelClass = "block mb-2 text-sm font-medium text-gray-900 dark:text-white";
        label.classList.add(...labelClass.split(" "));
        label.textContent = url + ":";
        return label;
    };

    $: hasPageNoFilter = false;
    const divId = `${platformName}-base`;
    onMount(async () => {
        const divEl = document.getElementById(divId) as HTMLDivElement;
        const textareaEl = divEl.querySelector("textarea") as HTMLTextAreaElement;
        const helperEl = document.getElementById("url-helper") as HTMLParagraphElement;
        const pageNoDivEl = document.getElementById("page-no") as HTMLDivElement;
        const pageNoInputsDivEl = document.getElementById("page-no-inputs") as HTMLDivElement;
        const pageNoFilterHelper = document.getElementById("page-no-filter-helper") as HTMLParagraphElement;
        pageNoFilterHelper.classList.add("hidden");

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
                helperEl.textContent = "Input Error: Invalid URL(s)!";
                textareaEl.classList.add("!border-red-500");
            }
        });

        const settingsCard = document.getElementById("settings-card") as HTMLDivElement;
        const getDownloadSettingsFromForm = (): Record<string, boolean | number> => {
            const checkboxes = settingsCard.querySelectorAll("input[type=checkbox]") as NodeListOf<HTMLInputElement>;
            const inputs = settingsCard.querySelectorAll("input") as NodeListOf<HTMLInputElement>;
            const downloadPreferences: Record<string, boolean | number> = {
                ArtworkType:        pixivArtworkType,
                RatingMode:         pixivRating,
                SearchMode:         pixivSearchMode,
                SortOrder:          pixivSortOrder,
                UgoiraOutputFormat: pixivUgoiraFormat,
            };

            for (const checkbox of checkboxes) {
                downloadPreferences[checkbox.name] = checkbox.checked;
            }
            for (const input of inputs) {
                if (input.type === "checkbox") {
                    continue;
                }

                if (input.type === "number") {
                    downloadPreferences[input.name] = parseInt(input.value);
                } else {
                    throw new Error("Unknown input type!");
                }
            }
            return downloadPreferences;
        };

        const addToQueueForm = document.getElementById("add-to-queue-form") as HTMLFormElement;
        addToQueueForm.addEventListener("submit", async (e: Event): Promise<void> => {
            e.preventDefault();

            const textareaInput = textareaEl.value;
            if (textareaInput === "") {
                helperEl.textContent = "Input Error: No URL(s)!";
                swal.fire({
                    title: "Input Error",
                    text: `No ${platformName} URL(s)!`,
                    icon: "error",
                });
                return;
            }

            const pageNoFilterIsValid = pageNoFilterHelper.classList.contains("hidden");
            if (!pageNoFilterIsValid) {
                swal.fire({
                    title: "Input Error",
                    text: "Invalid Page Number Filter Format!",
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
                helperEl.textContent = "Input Error: Invalid URL(s)!";
                swal.fire({
                    title: "Input Error",
                    text: `Invalid ${platformName} URL(s)!`,
                    icon: "error",
                });
                return;
            }

            swal.fire({
                title: "Adding to Queue...",
                text: "Please wait while the URL(s) are being processed and added to the download queue!",
                icon: "info",
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false,
                showConfirmButton: false,
                willOpen: () => {
                    swal.showLoading();
                },
            })

            try {
                await addToQueueFn(inputs, downloadPreferences);
                swal.fire({
                    title: "Added to Queue!",
                    text: "The URL(s) have been added to the download queue!",
                    icon: "success",
                });
                resetForm();
            } catch (e) {
                swal.close();
                if (e && e.toString().startsWith("no cookies found for")) {
                    swal.fire({
                        title: "Input Error",
                        text: `${e}. Please login first!`,
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
            <h4 class="capitalize">{platformTitle} Inputs</h4>
            <Hr />
            <Textarea 
                name="inputs"
                rows="6" 
                placeholder={`Input example:\n` + inputPlaceholder}
            />
            <div class="mt-2 text-right">
                <Helper id="url-helper" color="red" />
                <button type="submit" class="mt-2 btn btn-success" id="add-to-queue-btn">
                    <div class="flex">
                        <ArrowLeftOutline />
                        Add to queue!
                    </div>
                </button>
            </div>
        </Card>

        <Card class="mt-2 max-w-full max-h-[600px] overflow-y-auto {hasPageNoFilter ? "" : "hidden"}" id="page-no" size="xl">
            <h4>Page Numbers Filter</h4>
            <Hr />
            <Helper>Note that this is <strong>OPTIONAL</strong> as you can leave this <strong>EMPTY</strong> to download all pages!</Helper>
            <div class="mt-4 space-y-4" id="page-no-inputs"></div>
            <div class="mt-2 text-right">
                <Helper color="red" id="page-no-filter-helper">Invalid Filter Format!</Helper>
            </div>
        </Card>
    </form>

    <Card class="mt-2 max-w-full" size="xl" id="settings-card">
        <h4>Download Settings</h4>
        <Hr />
        {#await GetPreferences()}
            <div class="flex">
                <Spinner color="blue" /> <p class="ms-3">Loading form...</p>
            </div>
        {:then preferences}
            <Helper>This settings is for the current download inputs. However, you can save it globally by clicking "Save Settings" Button below!</Helper>
            <GeneralSettings promptSuccess={false} preferences={preferences}  />
            {#if platformName === actions.Pixiv}
            <Hr />
                <PixivSettings promptSuccess={false} preferences={preferences} bind:pixivArtworkType bind:pixivRating bind:pixivSearchMode bind:pixivAiSearchMode bind:pixivSortOrder bind:pixivUgoiraFormat />
            {/if}
            <Hr />
            <MergedSettings btnString="Save Settings Globally" />
        {/await}
    </Card>
</div>
