<script lang="ts">
    import { Input, Tooltip, ButtonGroup, Label } from "flowbite-svelte";
    import { UploadCookieFile, GetSessionValue, SetSessionValue, ResetSession } from "../../scripts/wailsjs/go/app/App";
    import { UploadSolid } from "flowbite-svelte-icons";
    import { swal } from "../../scripts/constants";
    import { onMount } from "svelte";
    import PasswordToggle from "../common/PasswordToggle.svelte";
    import ButtonGroupBtn from "../common/ButtonGroupBtn.svelte";

    export let elId: string;
    export let title: string;
    export let website: string;
    export let placeholder: string;

    let inpEl: HTMLInputElement;
    const saveSwalAlert = () => swal.fire({
        title: "Success",
        text: title + " session cookie saved successfully",
        icon: "success",
    })

    let deleteBtn: HTMLButtonElement;
    const toggleDeleteBtn = (val: string) => {
        if (val == "") {
            deleteBtn.classList.add("hidden");
        } else {
            deleteBtn.classList.remove("hidden");
        }
    }

    const updateInputValue = async () => {
        const sessionVal = await GetSessionValue(website);
        inpEl.value = sessionVal;
        toggleDeleteBtn(sessionVal)
    }

    onMount(async () => {
        inpEl = document.getElementById(elId) as HTMLInputElement;
        deleteBtn = document.getElementById(`${website}-delete-button`) as HTMLButtonElement;
        await updateInputValue();

        deleteBtn.addEventListener("click", () => {
            ResetSession(website)
                .then(() => {
                    inpEl.value = "";
                    deleteBtn.classList.add("hidden");
                    swal.fire({
                        title: "Success",
                        text: title + " saved session cookie deleted successfully",
                        icon: "success",
                    });
                })
        });

        const saveBtn = document.getElementById(`${website}-save-button`) as HTMLButtonElement;
        saveBtn.addEventListener("click", () => {
            const val = inpEl.value;
            SetSessionValue(website, val)
                .then(() => {
                    inpEl.value = val;
                    toggleDeleteBtn(val);
                    saveSwalAlert();
                });
        });
    });

    const UploadCookieFileWithAlert = () => {
        UploadCookieFile(website)
            .then(() => {
                updateInputValue();
                saveSwalAlert();
            }).catch((err) => {
                if (err == "no file selected") {
                    return;
                }

                swal.fire({
                    title: "Error",
                    text: err,
                    icon: "error",
                });
            });
    }
</script>

<div>
    <Label for={elId}>{title}</Label>
    <ButtonGroup class="w-full">
        <PasswordToggle elClass="w-full" hideByDefault={true}>
            <Input 
                class="mt-2" 
                name={elId} 
                id={elId} 
                type="text"
                placeholder={placeholder}
            />
        </PasswordToggle>
        <ButtonGroupBtn clickFn={UploadCookieFileWithAlert} elId="{website}-session-upload">
            <UploadSolid />
        </ButtonGroupBtn>
        <Tooltip triggeredBy="#{website}-session-upload">Upload Netscape/Mozilla generated cookie .txt file</Tooltip>
    </ButtonGroup>
    <div class="text-right mt-2">
        <button class="btn btn-danger hidden" id="{website}-delete-button">
            Reset
        </button>
        <button class="btn btn-success !me-0" id="{website}-save-button">
            Save
        </button>
    </div>
</div>
