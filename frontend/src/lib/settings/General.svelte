<script lang="ts">
    import bufferGif from "../../assets/images/buffer.gif";
    import { Input, Label, Helper, Fileupload, Hr } from "flowbite-svelte";
    import { swal, changeUsernameEventType } from "../../scripts/constants";
    import { GetFallbackUserProfileDataUrl } from "../../scripts/image";
    import { ChangeImgElSrcToFileData, Base64ImgStringToFile, ImgFileToDataURL } from "../../scripts/image";
    import { onMount, createEventDispatcher } from "svelte";
    import { PromptMasterPassword, GetUsername, SetMasterPassword, SetUsername, SelectProfilePic, UploadProfilePic, GetProfilePic, DeleteProfilePic } from "../../scripts/wailsjs/go/app/App";
    import { HasProfilePic } from "../../scripts/wailsjs/go/app/App";
    import PasswordToggle from "../common/PasswordToggle.svelte";

    export let username: string;

    const dispatcher = createEventDispatcher();
    const changeUsername = (newUsername: string): void => {
        dispatcher(changeUsernameEventType, newUsername);
    };

    onMount(async () => {
        const navbarUserProfile = document.getElementById("navbar-user-profile") as HTMLImageElement;

        const generalForm = document.getElementById("general-form") as HTMLFormElement;
        const profilePicResetBtn = document.getElementById("profile-pic-reset-btn") as HTMLButtonElement;

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

            profilePicResetBtn.classList.remove("hidden");
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

        username = await GetUsername() || "User";
        changeUsername(username);
        const usernameInput = document.getElementById("username") as HTMLInputElement;
        usernameInput.value = username;

        const resetGeneralForm = (): void => {
            generalForm.reset();
            usernameInput.value = username;
        };

        const handleGeneralFormSubmit = async (e: Event): Promise<void> => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const formData = new FormData(form);
            const file = formData.get("profile-image") as File;
            if (file.size > 0 && file.name !== "") {
                console.log("File:", file);
                await ChangeImgElSrcToFileData(profileImageEl, file);

                const base64URL = await ImgFileToDataURL(file);
                uploadedProfilePicURL = base64URL;
                navbarUserProfile.setAttribute("src", base64URL);

                const filePath = formData.get("profile-image-path") as string;
                if (filePath === "") {
                    throw new Error("Profile image path is empty");
                }
                await UploadProfilePic(filePath);
                hasProfilePic = true;
            }

            const newUsername = formData.get("username") as string;
            if (newUsername !== "") {
                await SetUsername(newUsername);
                changeUsername(newUsername);
                username = newUsername;
            }

            resetGeneralForm();
            profilePicResetBtn.classList.add("hidden");
            swal.fire({
                title: "Success",
                text: "Your profile has been updated.",
                icon: "success",
            });
        };

        const deleteProfileImageBtn = document.getElementById("delete-profile-image-btn") as HTMLButtonElement;
        if (!hasProfilePic) {
            deleteProfileImageBtn.classList.add("hidden");
        }
        const handleDeleteProfilePic = async (): Promise<void> => {
            if (!hasProfilePic) {
                return;
            }

            await DeleteProfilePic();
            hasProfilePic = false;
            uploadedProfilePicURL = "";
            resetGeneralForm();
            navbarUserProfile.src = await GetFallbackUserProfileDataUrl();
            profileImageEl.src = await GetFallbackUserProfileDataUrl();
            profilePicResetBtn.classList.add("hidden");
            deleteProfileImageBtn.classList.add("hidden");
        };

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
            resetGeneralForm();
            profileImageEl.src = hasProfilePic ? uploadedProfilePicURL : await GetFallbackUserProfileDataUrl();
            profilePicResetBtn.classList.add("hidden");
        };

        generalForm.addEventListener("submit", handleGeneralFormSubmit);
        profileImageInput.addEventListener("change", changeProfilePicPreview);
        profilePicResetBtn.addEventListener("click", resetProfilePic);
        deleteProfileImageBtn.addEventListener("click", handleDeleteProfilePic);
    });

    onMount(async () => {
        const masterPasswordForm = document.getElementById("master-password-form") as HTMLFormElement;
        const masterPasswordFormResetBtn = document.getElementById("master-password-form-reset-btn") as HTMLButtonElement;
        const hasMasterPassword = await PromptMasterPassword();

        const handleMasterPasswordFormSubmit = async (e: Event): Promise<void> => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const formData = new FormData(form);
            const masterPassword = formData.get("master-password") as string;

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

        const masterPasswordDefault = hasMasterPassword ? "********" : "";
        const masterPasswordInput = document.getElementById("master-password") as HTMLInputElement;
        const resetMasterPasswordForm = (): void => {
            if (!hasMasterPassword) {
                masterPasswordInput.value = masterPasswordDefault;
                return;
            }
        };
        if (masterPasswordInput && hasMasterPassword) {
            // TODO: make the masterPasswordInput disabled first unless user clicks on the edit button
            masterPasswordInput.value = masterPasswordDefault;
            masterPasswordInput.disabled = true;
        }

        masterPasswordForm.addEventListener("submit", handleMasterPasswordFormSubmit);
        masterPasswordFormResetBtn.addEventListener("click", resetMasterPasswordForm);
    });
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="mx-auto text-center">
        <img class="rounded-full w-32 h-32 border-4 mt-2 border-gray-200" id="profile-img-el" alt="user profile" src="{bufferGif}" />
        <button id="profile-pic-reset-btn" class="text-small hidden text-red-500 hover:text-red-600">Reset Image</button>
    </div>
    <form class="md:col-span-3" id="general-form">
        <div class="flex">
            <div class="w-full">
                <Label for="username" class="pb-2">Username:</Label>
                <Input name="username" id="username" />
            </div>
        </div>
        <div class="flex mt-4">
            <div class="w-full">
                <Label for="profile-image" class="pb-2">Upload file</Label>
                <Fileupload name="profile-image" id="profile-image" class="mb-2" />
                <Helper>PNG, JPG, GIF or WEBP.</Helper>
                <Input name="profile-image-path" id="profile-image-path" type="hidden" />
                <button type="submit" class="btn btn-success mt-4 float-end">Save</button>
                <button id="delete-profile-image-btn" type="button" class="btn btn-danger mt-4 float-end">Reset</button>
            </div>
        </div>
    </form>
    <form class="md:col-start-2 md:col-span-3" id="master-password-form">
        <Hr />
        <div class="flex mt-4">
            <div class="w-full">
                <Label for="master-password" class="pb-2">Master Password:</Label>
                <PasswordToggle inputId="master-password">
                    <Input name="master-password" id="master-password" type="password" />
                </PasswordToggle>
            </div>
        </div>
        <div class="flex">
            <div class="mt-4 w-full hidden" id="current-master-password-div">
                <Label for="current-master-password" class="pb-2">Current Master Password:</Label>
                <PasswordToggle inputId="current-master-password">
                    <Input name="current-master-password" id="current-master-password" type="password" />
                </PasswordToggle>
            </div>
        </div>
        <div class="flex">
            <div class="mt-4 w-full hidden" id="new-master-password-div">
                <Label for="new-master-password" class="pb-2">New Master Password:</Label>
                <PasswordToggle inputId="new-master-password">
                    <Input name="new-master-password" id="new-master-password" type="password" />
                </PasswordToggle>
            </div>
        </div>
        <div class="text-right mt-4">
            <button id="master-password-form-reset-btn" type="button" class="btn btn-danger">Reset</button>
            <button type="submit" class="btn btn-success">Save</button>
        </div>
    </form>
</div>
