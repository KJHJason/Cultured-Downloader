<script lang="ts">
    import { onMount } from "svelte";
    import { Textarea, Helper, Card, Hr  } from "flowbite-svelte";
    import { swal } from "../scripts/constants";
    import { ArrowDownToBracketSolid } from "flowbite-svelte-icons";

    export let platformName: string;
    export let inputPlaceholder: string;
    export let urlValidationFn: (textareaInput: string) => boolean;
    export let settingConfigFn: () => Promise<void>;

    onMount(() => {
        settingConfigFn();
    });

    const divId = `${platformName}-base`;
    onMount(() => {
        const divEl = document.getElementById(divId) as HTMLDivElement;
        const textareaEl = divEl.querySelector("textarea") as HTMLTextAreaElement;
        const helperEl = document.getElementById("url-helper") as HTMLParagraphElement;

        textareaEl.addEventListener("input", () => {
            const textareaInput = textareaEl.value;
            if (!textareaInput) {
                helperEl.textContent = "";
                return;
            }

            const isValid = urlValidationFn(textareaInput);
            helperEl.textContent = isValid ? "" : "Input Error: Invalid URL(s)!";
        });

        const buttonEl = document.getElementById("add-to-queue-btn") as HTMLButtonElement;
        buttonEl.addEventListener("click", () => {
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

            // TODO: Add to queue
        });
    });
</script>

<div class="container mx-auto" id={divId}>
    <Card class="max-w-full" size="xl">
        <h4>{platformName} URLs</h4>
        <Hr />
        <Textarea 
            rows="8" 
            placeholder={`Input example:\n` + inputPlaceholder}
        />
        <div class="mt-2 text-right">
            <Helper id="url-helper" color="red"></Helper>
            <button class="mt-2 btn btn-success" id="add-to-queue-btn">
                <div class="flex">
                    <ArrowDownToBracketSolid />
                    Add to queue!
                </div>
            </button>
        </div>
    </Card>

    <Card class="mt-4 max-w-full" size="xl">
        <h4>Download Settings</h4>
        <Hr />
        <slot />
    </Card>
</div>
