<script lang="ts">
    import { onMount } from "svelte";
    import { Textarea, Helper, Card, Hr, Checkbox  } from "flowbite-svelte";
    import { swal } from "../scripts/constants";
    import { ArrowDownToBracketSolid } from "flowbite-svelte-icons";

    export let platformName: string;
    export let inputPlaceholder: string;
    export let urlValidationFn: (urls: string | string[]) => boolean;
    export let checkUrlHasPageNumFilter: (inputUrl: string) => boolean;
    export let settingConfigFn: () => Promise<void>;

    onMount(() => {
        settingConfigFn();
    });

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
    onMount(() => {
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

                    const inputRegex = /^\d+(-\d+)?$/;
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
        textareaEl.addEventListener("input", () => {
            const textareaInput = textareaEl.value;
            pageNoFilterHelper.classList.add("hidden");
            if (!textareaInput) {
                resetForm();
                return;
            }

            const urls = textareaInput.split("\n");
            const uniqueUrls = Array.from(new Set(urls));
            textareaEl.value = uniqueUrls.join("\n");

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

            const isValid = urlValidationFn(uniqueUrls);
            if (isValid) {
                helperEl.textContent = "";
                textareaEl.classList.remove("!border-red-500");
            } else {
                helperEl.textContent = "Input Error: Invalid URL(s)!";
                textareaEl.classList.add("!border-red-500");
            }
        });

        const addToQueueForm = document.getElementById("add-to-queue-form") as HTMLFormElement;
        addToQueueForm.addEventListener("submit", (e: Event): void => {
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

            const isValid = urlValidationFn(textareaInput);
            if (!isValid) {
                helperEl.textContent = "Input Error: Invalid URL(s)!";
                swal.fire({
                    title: "Input Error",
                    text: `Invalid ${platformName} URL(s)!`,
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

            const formData = new FormData(addToQueueForm);

            // TODO: Add to queue in backend
            swal.fire({
                title: "Added to Queue!",
                text: "The URL(s) have been added to the download queue!",
                icon: "success",
            });
            resetForm();
        });
    });
</script>

<div class="container mx-auto" id={divId}>
    <form id="add-to-queue-form">
        <Card class="max-w-full" size="xl">
            <h4>{platformName} URLs</h4>
            <Hr />
            <Textarea 
                rows="6" 
                placeholder={`Input example:\n` + inputPlaceholder}
            />
            <div class="mt-2 text-right">
                <Helper id="url-helper" color="red" />
                <button type="submit" class="mt-2 btn btn-success" id="add-to-queue-btn">
                    <div class="flex">
                        <ArrowDownToBracketSolid />
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

    <Card class="mt-2 max-w-full" size="xl">
        <h4>Download Settings</h4>
        <Hr />
        <Helper>This settings is for the current download inputs. However, you can save it globally by clicking "Save Settings" Button below!</Helper>
        <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 ">
            <Checkbox name="dl-post-thumbnail" id="dl-post-thumbnail">Post Thumbnail</Checkbox>
            <Checkbox name="dl-post-images" id="dl-post-images">Post Images</Checkbox>
            <Checkbox name="dl-post-attachments" id="dl-post-attachments">Post Attachments</Checkbox>
            <Checkbox name="dl-gdrive-links" id="dl-gdrive-links">Overwrite Files</Checkbox>
            <slot />
        </div>
        <Hr />
        <div class="text-right">
            <button class="btn btn-success">Save Settings Globally</button>
        </div>
    </Card>
</div>
