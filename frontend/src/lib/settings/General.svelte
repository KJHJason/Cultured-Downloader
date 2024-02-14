<script lang="ts">
    import { Input, Label, Helper, Fileupload, Hr } from "flowbite-svelte";
    import { swal, changeUsernameEventType } from "../../scripts/constants";
    import { GetFallbackUserProfileDataUrl } from "../../scripts/image";
    import bufferGif from "../../assets/images/buffer.gif";
    import { ChangeImgElSrcToFileData, GetBase64ImgStringFromFile, Base64ImgStringToFile, ImgFileToDataURL } from "../../scripts/image";
    import { onMount, createEventDispatcher } from "svelte";
    import { PromptMasterPassword, GetUsername, SetMasterPassword, SetUsername, SelectProfilePic, UploadProfilePic, GetProfilePic, DeleteProfilePic } from "../../scripts/wailsjs/go/app/App";
    import { HasProfilePic } from "../../scripts/wailsjs/go/app/App";

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
        const navbarUserProfile = document.getElementById("navbar-user-profile") as HTMLImageElement;

        const profilePicForm = document.getElementById("profile-pic-form") as HTMLFormElement;
        const profilePicFormResetBtn = document.getElementById("profile-pic-reset-btn") as HTMLButtonElement;
        const generalForm = document.getElementById("general-form") as HTMLFormElement;
        const generalFormResetBtn = document.getElementById("general-form-reset-btn") as HTMLButtonElement;

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
            const file = Base64ImgStringToFile(profilePicData, profilePicFilename, profilePicType);

            const container = new DataTransfer();
            container.items.add(file);
            profileImageInput.files = container.files;

            // trigger change event
            const event = new Event("change", { bubbles: true });
            profileImageInput.dispatchEvent(event);

            profilePicFormResetBtn.classList.remove("invisible");
        });

        const profileImageEl = document.getElementById("profile-img-el") as HTMLImageElement;
        const changeProfilePicPreview = async (e: Event): Promise<void> => {
            const fileTarget = e.target as HTMLInputElement;
            if (!fileTarget.files) {
                return;
            }
            const file = fileTarget.files[0];
            await ChangeImgElSrcToFileData(profileImageEl, file);
        };

        let uploadedProfilePicURL: string;
        let hasProfilePic = await HasProfilePic();
        const handleProfilePicFormSubmit = async (e: Event): Promise<void> => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const formData = new FormData(form);
            const file = formData.get("profile-image") as File;
            await ChangeImgElSrcToFileData(profileImageEl, file);

            const base64URL = await ImgFileToDataURL(file);
            uploadedProfilePicURL = base64URL;
            navbarUserProfile.setAttribute("src", base64URL);

            const filePath = formData.get("profile-image-path") as string;
            await UploadProfilePic(filePath);
            hasProfilePic = true;
            profilePicForm.reset();
            profilePicFormResetBtn.classList.add("invisible");
            swal.fire({
                title: "Success",
                text: "Profile picture has been updated.",
                icon: "success",
            });
        };

        const deleteProfileImageBtn = document.getElementById("delete-profile-image-btn") as HTMLButtonElement;
        if (!hasProfilePic) {
            deleteProfileImageBtn.classList.add("invisible");
        }
        const handleDeleteProfilePic = async (): Promise<void> => {
            if (!hasProfilePic) {
                return;
            }

            await DeleteProfilePic();
            hasProfilePic = false;
            uploadedProfilePicURL = "";
            navbarUserProfile.src = await GetFallbackUserProfileDataUrl();
            profileImageEl.src = await GetFallbackUserProfileDataUrl();
            profilePicFormResetBtn.classList.add("invisible");
            deleteProfileImageBtn.classList.add("invisible");
        };

        username = await GetUsername() || "User";
        changeUsername(username);

        if (hasProfilePic) {
            const { Data, Type } = await GetProfilePic();;
            const mimetype = `image/${Type}`;
            // const dumpedJSON = JSON.stringify({ data: Data, mimetype });
            // console.log("Profile pic data:", dumpedJSON);
            // changeProfilePic(dumpedJSON);

            const file = Base64ImgStringToFile(Data, "profile-pic.png", mimetype);
            uploadedProfilePicURL = await ImgFileToDataURL(file);
            navbarUserProfile.src = uploadedProfilePicURL;
            profileImageEl.src = uploadedProfilePicURL;
        } else {
            profileImageEl.src = await GetFallbackUserProfileDataUrl();
        }

        const resetProfilePic = async (): Promise<void> => {
            profilePicForm.reset();
            profileImageEl.src = hasProfilePic ? uploadedProfilePicURL : await GetFallbackUserProfileDataUrl();
            profilePicFormResetBtn.classList.add("invisible");
        };

        const hasMasterPassword = await PromptMasterPassword();
        const masterPasswordDefault = hasMasterPassword ? "********" : "";
        const usernameInput = document.getElementById("username") as HTMLInputElement;
        const masterPasswordInput = document.getElementById("master-password") as HTMLInputElement;
        const resetGeneralForm = (): void => {
            usernameInput.value = username;
            masterPasswordInput.value = masterPasswordDefault;
        };
        usernameInput.value = username;
        if (masterPasswordInput && hasMasterPassword) {
            // TODO: make the masterPasswordInput disabled first unless user clicks on the edit button
            masterPasswordInput.value = masterPasswordDefault;
            masterPasswordInput.disabled = true;
        }

        profilePicForm.addEventListener("submit", handleProfilePicFormSubmit);
        profilePicForm.addEventListener("change", changeProfilePicPreview);
        profilePicFormResetBtn.addEventListener("click", resetProfilePic);
        generalForm.addEventListener("submit", handleGeneralFormSubmit);
        generalFormResetBtn.addEventListener("click", resetGeneralForm);
        deleteProfileImageBtn.addEventListener("click", handleDeleteProfilePic);
    });
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="mx-auto text-center">
        <img class="rounded-full w-32 h-32 border-4 mt-2 border-gray-200" id="profile-img-el" alt="user profile" src="{bufferGif}" />
        <button id="profile-pic-reset-btn" class="text-small invisible text-red-500 hover:text-red-600">Reset Image</button>
    </div>
    <form class="md:col-span-3 flex items-center" id="profile-pic-form">
        <div class="w-full">
            <Label for="profile-image" class="pb-2">Upload file</Label>
            <Fileupload name="profile-image" id="profile-image" required class="mb-2" />
            <Helper>SVG, PNG, JPG or GIF.</Helper>
            <Input name="profile-image-path" id="profile-image-path" type="hidden" required />
            <button type="submit" class="btn btn-success mt-4 float-end">Save</button>
            <button id="delete-profile-image-btn" type="button" class="btn btn-danger mt-4 float-end">Delete</button>
        </div>
    </form>
    <form class="md:col-start-2 md:col-span-3" id="general-form">
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
            <button id="general-form-reset-btn" type="button" class="btn btn-danger">Reset</button>
            <button type="submit" class="btn btn-success">Save</button>
        </div>
    </form>
</div>
