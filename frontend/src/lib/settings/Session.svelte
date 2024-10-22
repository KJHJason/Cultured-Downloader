<script lang="ts">
    import { Input, Tooltip, ButtonGroup, Label, Helper } from "flowbite-svelte";
    import { UploadCookieFile, GetSessionValue, SetSessionValue, ResetSession } from "../../scripts/wailsjs/go/app/App";
    import { UploadSolid } from "flowbite-svelte-icons";
    import { swal, pleaseWaitSwal } from "../../scripts/constants";
    import { onMount } from "svelte";
    import PasswordToggle from "../common/PasswordToggle.svelte";
    import ButtonGroupBtn from "../common/ButtonGroupBtn.svelte";
    import { translateText } from "../../scripts/language";

    interface Props {
        elId: string;
        title: string;
        website: string;
        placeholder: string;
        translatedDeleteBtnText: string;
        translatedSaveBtnText: string;
        translatedUploadBtnText: string;
        translatedPixivOauthText: string;
        translatedSavedSessionCookieText: string;
        translatedDeletedSessionCookieText: string;
        translatedErrText: string;
    }

    let {
        elId,
        title,
        website,
        placeholder,
        translatedDeleteBtnText,
        translatedSaveBtnText,
        translatedUploadBtnText,
        translatedPixivOauthText,
        translatedSavedSessionCookieText,
        translatedDeletedSessionCookieText,
        translatedErrText
    }: Props = $props();

    let inpEl: HTMLInputElement;
    const saveSwalAlert = () => swal.fire({
        title: title,
        text: translatedSavedSessionCookieText,
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

    let savingText: string;
    let pleaseWaitText: string;
    onMount(async () => {
        savingText = await translateText("Saving...");
        pleaseWaitText = await translateText("Please wait a moment.");

        inpEl = document.getElementById(elId) as HTMLInputElement;
        deleteBtn = document.getElementById(`${website}-delete-button`) as HTMLButtonElement;
        await updateInputValue();

        deleteBtn.addEventListener("click", () => {
            ResetSession(website)
                .then(() => {
                    inpEl.value = "";
                    deleteBtn.classList.add("hidden");
                    swal.fire({
                        title: title,
                        text: translatedDeletedSessionCookieText,
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
        pleaseWaitSwal.fire({
            title: savingText,
            text: pleaseWaitText,
        })
        UploadCookieFile(website)
            .then(() => {
                updateInputValue();
                saveSwalAlert();
            }).catch((err) => {
                if (err == "no file selected") {
                    return;
                }

                swal.fire({
                    title: translatedErrText,
                    text: err,
                    icon: "error",
                });
            });
    }
</script>

<div>
    <Label for={elId}>{title}:</Label>
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
        <Tooltip triggeredBy="#{website}-session-upload">{translatedUploadBtnText}</Tooltip>
    </ButtonGroup>
    {#if website === "pixiv"}
        <Helper class="mt-1">
            *{translatedPixivOauthText}
        </Helper>
    {/if}
    <div class="text-right mt-2">
        <button class="btn btn-danger hidden" id="{website}-delete-button">
            {translatedDeleteBtnText}
        </button>
        <button class="btn btn-success !me-0" id="{website}-save-button">
            {translatedSaveBtnText}
        </button>
    </div>
</div>
