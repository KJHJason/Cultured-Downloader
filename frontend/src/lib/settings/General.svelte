<script lang="ts">
    import { Input, Label, Helper, Fileupload, Hr } from "flowbite-svelte";
    import { fallbackUserProfile, swal } from "../../scripts/constants";
    import { onMount } from "svelte";
    import { SetMasterPassword } from "../../scripts/wailsjs/go/app/App";

    const enableSweetAlert2Theme = (theme: string) => {
        document.head.querySelector('#swal2-theme-styles')?.setAttribute('href', `@sweetalert2/theme-${theme}/${theme}.css`)
    }

    const handleProfilePicFormSubmit = (e: Event): void => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        const file = formData.get("profile-image") as File;
        const reader = new FileReader();
        reader.onload = (e: ProgressEvent<FileReader>): void => {
            const target = e.target as FileReader;
            const result = target.result as string;
            const photo = document.getElementById("photo") as HTMLImageElement;
            photo.src = result;
        };
        reader.readAsDataURL(file);

        // Send form data to server
    };

    const handleGeneralFormSubmit = async (e: Event): Promise<void> => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        const username = formData.get("username") as string;
        const masterPassword = formData.get("master-password") as string;

        // Send form data to server
        try {
            await SetMasterPassword(masterPassword);
        } catch (e) {
            console.error(e);
            swal.fire({
                title: "Error",
                text: "An error occurred while setting the master password. Please try again later.",
                icon: "error",
            });
        }
    };

    const resetProfilePic = (): void => {
        const photo = document.getElementById("photo") as HTMLImageElement;
        photo.src = fallbackUserProfile;
    };

    const resetGeneralForm = (): void => {
        const username = document.getElementById("username") as HTMLInputElement;
        const masterPassword = document.getElementById("master-password") as HTMLInputElement;
        username.value = "";
        masterPassword.value = "";
    };

    onMount(() => {
        const profilePicForm = document.getElementById("profilePicForm") as HTMLFormElement;
        const profilePicFormResetBtn = document.getElementById("profilePicFormResetBtn") as HTMLButtonElement;
        const generalForm = document.getElementById("generalForm") as HTMLFormElement;
        const generalFormResetBtn = document.getElementById("generalFormResetBtn") as HTMLButtonElement;
        
        profilePicForm.addEventListener("submit", handleProfilePicFormSubmit);
        profilePicFormResetBtn.addEventListener("click", resetProfilePic);
        generalForm.addEventListener("submit", handleGeneralFormSubmit);
        generalFormResetBtn.addEventListener("click", resetGeneralForm);
    });

    
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="mx-auto text-center">
        <img class="rounded-full w-32 h-32 border-4 mt-2 border-gray-200" id="photo" src="{fallbackUserProfile}" alt="test">
        <button id="profilePicFormResetBtn" class="text-small text-red-500 hover:text-red-600">Reset Image</button>
    </div>
    <form class="md:col-span-3 flex items-center" id="profilePicForm">
        <div class="w-full">
            <Label for="profile-image" class="pb-2">Upload file</Label>
            <Fileupload id="profile-image" class="mb-2" />
            <Helper>SVG, PNG, JPG or GIF.</Helper>
            <button type="submit" class="btn btn-success mt-4 float-end">Save</button>
        </div>
    </form>
    <form class="md:col-start-2 md:col-span-3" id="generalForm">
        <div class="flex">
            <div class="w-full">
                <Hr />
                <Label for="username" class="pb-2">Username:</Label>
                <Input id="username" />
            </div>
        </div>
        <div class="flex mt-4">
            <div class="w-full">
                <Label for="master-password" class="pb-2">Master Password:</Label>
                <Input id="master-password" />
            </div>
        </div>
        <div class="mt-4 text-right">
            <button id="generalFormResetBtn" type="button" class="btn btn-danger">Reset</button>
            <button type="submit" class="btn btn-success">Save</button>
        </div>
    </form>
</div>
