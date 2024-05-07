<script lang="ts">
    import { onMount } from "svelte";
    import { generalFormId, pixivFormId, swal } from "../../scripts/constants";
    import { Translate } from "../../scripts/language";

    export let btnString: string;
    export let customGeneralFormId = generalFormId;
    export let customPixivFormId = pixivFormId;

    onMount(() => {
        let generalForm: HTMLFormElement;
        let pixivForm: HTMLFormElement;

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
                    title: "Error",
                    text: "Forms not loaded yet... Please wait a moment and try again.",
                    icon: "error",
                });
                return;
            }

            generalForm?.dispatchEvent(new Event("submit"));
            pixivForm?.dispatchEvent(new Event("submit"));
            swal.fire({
                title: "Success",
                text: "Preferences saved successfully",
                icon: "success",
            });
        });
    });
</script>

<div class="text-right mt-4">
    <button class="btn btn-success" id="save-all-btn">
        {Translate(btnString)}
    </button>
</div>
