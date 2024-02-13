<script lang="ts">
    import { Input, Label, Helper, Fileupload, Hr } from "flowbite-svelte";
    import { fallbackUserProfile, swal, changeUsernameEventType } from "../../scripts/constants";
    import { onMount, createEventDispatcher } from "svelte";
    import { GetUsername, SetMasterPassword, SetUsername, SelectProfilePic, UploadProfilePic } from "../../scripts/wailsjs/go/app/App";

    export let username: string;

    const dispatcher = createEventDispatcher();
    const changeUsername = (newUsername: string): void => {
        dispatcher(changeUsernameEventType, newUsername);
    };

    const handleGeneralFormSubmit = async (e: Event): Promise<void> => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        const newUsername = formData.get("username") as string;
        const masterPassword = formData.get("master-password") as string;

        try {
            if (newUsername !== "") {
                await SetUsername(newUsername);
                changeUsername(newUsername);
                swal.fire({
                    title: "Success",
                    text: "Username has been updated.",
                    icon: "success",
                });
            }
        } catch (e) {
            console.error(e);
            swal.fire({
                title: "Error",
                text: "An error occurred while setting the username. Please try again later.",
                icon: "error",
            });
        }

        try {
            if (masterPassword !== "") {
                await SetMasterPassword(masterPassword);
                swal.fire({
                    title: "Success",
                    text: "Master password has been updated.",
                    icon: "success",
                });
            }
        } catch (e) {
            console.error(e);
            swal.fire({
                title: "Error",
                text: "An error occurred while setting the master password. Please try again later.",
                icon: "error",
            });
        }
    };

    onMount(async () => {
        const profilePicForm = document.getElementById("profilePicForm") as HTMLFormElement;
        const profilePicFormResetBtn = document.getElementById("profilePicFormResetBtn") as HTMLButtonElement;
        const generalForm = document.getElementById("generalForm") as HTMLFormElement;
        const generalFormResetBtn = document.getElementById("generalFormResetBtn") as HTMLButtonElement;

        const photo = document.getElementById("photo") as HTMLImageElement;
        const resetProfilePic = (): void => {
            profilePicForm.reset();
            photo.src = fallbackUserProfile;
        };

        const profileImagePathInput = document.getElementById("profile-image-path") as HTMLInputElement;
        const profileImageInput = document.getElementById("profile-image") as HTMLInputElement;
        profileImageInput.addEventListener("click", async (e: Event) => { 
            e.preventDefault();
            const profilePicInfo = await SelectProfilePic();
            const profilePicPath = profilePicInfo.Path as string;
            const profilePicFilename = profilePicInfo.Filename as string;
            const profilePicType = profilePicInfo.Type as string;
            const profilePicData = profilePicInfo.Data as string; // base64 encoded string

            if (!profilePicPath) {
                return;
            }

            profileImagePathInput.value = profilePicPath;
            const mimetype = `image/${profilePicType}`;
            const binaryData = Uint8Array.from(atob(profilePicData), c => c.charCodeAt(0)); // decode base64 string
            const file = new File([binaryData], profilePicFilename, { type: mimetype });

            const container = new DataTransfer();
            container.items.add(file);
            profileImageInput.files = container.files;

            // trigger change event
            const event = new Event("change", { bubbles: true });
            profileImageInput.dispatchEvent(event);
        });

        const profileImageEl = document.getElementById("profile-img-el") as HTMLInputElement;
        const changeProfilePicPreviewLogic = (file: File): void => {
            const reader = new FileReader();
            reader.onload = (e: ProgressEvent<FileReader>): void => {
                const target = e.target as FileReader;
                const result = target.result as string;
                profileImageEl.src = result;
            };
            reader.readAsDataURL(file);
        };

        const changeProfilePicPreview = (e: Event): void => {
            const fileTarget = e.target as HTMLInputElement;
            if (!fileTarget.files) {
                return;
            }
            const file = fileTarget.files[0];
            changeProfilePicPreviewLogic(file);
        };

        const handleProfilePicFormSubmit = async (e: Event): Promise<void> => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const formData = new FormData(form);
            const file = formData.get("profile-image") as File;
            changeProfilePicPreviewLogic(file);

            const filePath = formData.get("profile-image-path") as string;
            await UploadProfilePic(filePath);
        };

        username = await GetUsername() || "User";
        changeUsername(username);

        const usernameInput = document.getElementById("username") as HTMLInputElement;
        const masterPasswordInput = document.getElementById("master-password") as HTMLInputElement;
        const resetGeneralForm = (): void => {
            usernameInput.value = username;
            masterPasswordInput.value = "";
        };
        console.log("username", username);
        usernameInput.value = username;

        profilePicForm.addEventListener("submit", handleProfilePicFormSubmit);
        profilePicForm.addEventListener("change", changeProfilePicPreview);
        profilePicFormResetBtn.addEventListener("click", resetProfilePic);
        generalForm.addEventListener("submit", handleGeneralFormSubmit);
        generalFormResetBtn.addEventListener("click", resetGeneralForm);
    });
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="mx-auto text-center">
        <img class="rounded-full w-32 h-32 border-4 mt-2 border-gray-200" id="profile-img-el" src="{fallbackUserProfile}" alt="user profile" />
        <button id="profilePicFormResetBtn" class="text-small text-red-500 hover:text-red-600">Reset Image</button>
    </div>
    <form class="md:col-span-3 flex items-center" id="profilePicForm">
        <div class="w-full">
            <Label for="profile-image" class="pb-2">Upload file</Label>
            <Fileupload name="profile-image" id="profile-image" required class="mb-2" />
            <Helper>SVG, PNG, JPG or GIF.</Helper>
            <Input name="profile-image-path" id="profile-image-path" type="hidden" required />
            <button type="submit" class="btn btn-success mt-4 float-end">Save</button>
        </div>
    </form>
    <form class="md:col-start-2 md:col-span-3" id="generalForm">
        <div class="flex">
            <div class="w-full">
                <Hr />
                <Label for="username" class="pb-2">Username:</Label>
                <Input name="username" id="username" />
            </div>
        </div>
        <div class="flex mt-4">
            <div class="w-full">
                <Label for="master-password" class="pb-2">Master Password:</Label>
                <Input name="master-password" id="master-password" />
            </div>
        </div>
        <div class="mt-4 text-right">
            <button id="generalFormResetBtn" type="button" class="btn btn-danger">Reset</button>
            <button type="submit" class="btn btn-success">Save</button>
        </div>
    </form>
</div>
