<script lang="ts">
    import { onMount } from "svelte";
    import { generalFormId, pixivFormId, swal } from "../../scripts/constants";
    import { translate, translateText } from "../../scripts/language";

    export let btnString: string;
    export let customGeneralFormId = generalFormId;
    export let customPixivFormId = pixivFormId;

    onMount(async () => {
        let generalForm: HTMLFormElement;
        let pixivForm: HTMLFormElement;

        const success = await translateText("Success");
        const prefsSaved = await translateText("Preferences saved successfully");
        const error = await translateText("Error");
        const formsNotLoaded = await translateText("Forms not loaded yet... Please wait a moment and try again.");

        const saveAllBtn = document.getElementById("save-all-btn") as HTMLButtonElement;
        saveAllBtn.addEventListener("click", () => {
            if (!generalForm) {
                generalForm = document.getElementById(customGeneralFormId) as HTMLFormElement;
            }
            if (!pixivForm) {
                pixivForm = document.getElementById(customPixivFormId) as HTMLFormElement;
            }

            if (!generalForm && !pixivForm) {
                swal.fire({
                    title: error,
                    text: formsNotLoaded,
                    icon: "error",
                });
                return;
            }

            generalForm?.dispatchEvent(new Event("submit"));
            pixivForm?.dispatchEvent(new Event("submit"));
            swal.fire({
                title: success,
                text: prefsSaved,
                icon: "success",
            });
        });
    });
</script>

<div class="text-right mt-4">
    <button class="btn btn-success" id="save-all-btn">
        {translate(btnString, "save-all-btn")}
    </button>
</div>
