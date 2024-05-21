<script lang="ts">
    import bufferGif from "../../assets/images/buffer.gif";
    import { Input, Label, Helper, Fileupload, Hr, Select, ButtonGroup } from "flowbite-svelte";
    import Swal from "sweetalert2";
    import { swal, invertedSwal } from "../../scripts/constants";
    import { GetFallbackUserProfileDataUrl, GetProfilePicURL, ChangeImgElSrcToFileData, Base64ImgStringToFile, ImgFileToDataURL } from "../../scripts/image";
    import { LANGUAGES, translate, translateText } from "../../scripts/language";
    import Translate from "../common/Translate.svelte";
    import { onMount } from "svelte";
    import PasswordToggle from "../common/PasswordToggle.svelte";
    import {
        PromptMasterPassword,
        CheckMasterPassword,
        ChangeMasterPassword,
        RemoveMasterPassword,
        SetMasterPassword,
        SetUsername,
        SelectProfilePic,
        UploadProfilePic,
        DeleteProfilePic,
        HasProfilePic,
        GetLanguage,
        SetLanguage,
    } from "../../scripts/wailsjs/go/app/App";
    import { LogError } from "../../scripts/wailsjs/runtime/runtime";
    import type { Writable } from "svelte/store";

    let lang = "";
    export let username: Writable<string>;
    export let language: Writable<string>;

    onMount(async () => {
        lang = await GetLanguage();
        const navbarUserProfile = document.getElementById("navbar-user-profile") as HTMLImageElement;

        const generalForm = document.getElementById("general-form") as HTMLFormElement;
        const profilePicResetBtn = document.getElementById("profile-pic-reset-btn") as HTMLButtonElement;

        const profileImagePathInput = document.getElementById("profile-image-path") as HTMLInputElement;
        const profileImageInput = document.getElementById("profile-image") as HTMLInputElement;
        profileImageInput.addEventListener("click", async (e: Event) => { 
            e.preventDefault();
            const profilePicInfo = await SelectProfilePic();
            const profilePicPath = profilePicInfo.Path;
            const profilePicFilename = profilePicInfo.Filename;
            const profilePicType = profilePicInfo.Type;
            const profilePicData = profilePicInfo.Data; // base64 encoded string

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

        const usernameInput = document.getElementById("username") as HTMLInputElement;
        usernameInput.value = $username;

        const resetImageInputs = (): void => {
            // not using generalForm.reset() as it will reset the select element to the first option
            profileImageInput.value = "";
            profileImagePathInput.value = "";
        };

        const handleGeneralFormSubmit = async (e: Event): Promise<void> => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const formData = new FormData(form);
            const file = formData.get("profile-image") as File;
            if (file.size > 0 && file.name !== "") {
                await ChangeImgElSrcToFileData(profileImageEl, file);

                const base64URL = await ImgFileToDataURL(file);
                uploadedProfilePicURL = base64URL;
                navbarUserProfile.setAttribute("src", base64URL);

                const filePath = formData.get("profile-image-path") as string;
                if (filePath === "") {
                    throw new Error(await translateText("Profile image path is empty"));
                }
                await UploadProfilePic(filePath);
                hasProfilePic = true;
            }

            const newUsername = formData.get("username") as string;
            if (newUsername !== "") {
                await SetUsername(newUsername);
                username.set(newUsername);
            }

            if (lang !== $language) {
                await SetLanguage(lang);
                language.set(lang);
            }

            resetImageInputs();
            profilePicResetBtn.classList.add("hidden");
            swal.fire({
                title: await translateText("Success"),
                text: await translateText("Your profile has been updated."),
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
            resetImageInputs();
            navbarUserProfile.src = await GetFallbackUserProfileDataUrl();
            profileImageEl.src = await GetFallbackUserProfileDataUrl();
            profilePicResetBtn.classList.add("hidden");
            deleteProfileImageBtn.classList.add("hidden");
        };

        if (hasProfilePic) {
            uploadedProfilePicURL = await GetProfilePicURL(true);
            navbarUserProfile.src = uploadedProfilePicURL;
            profileImageEl.src = uploadedProfilePicURL;
        } else {
            profileImageEl.src = await GetFallbackUserProfileDataUrl();
        }

        const resetProfilePic = async (): Promise<void> => {
            resetImageInputs();
            profileImageEl.src = hasProfilePic ? uploadedProfilePicURL : await GetFallbackUserProfileDataUrl();
            profilePicResetBtn.classList.add("hidden");
        };

        generalForm.addEventListener("submit", handleGeneralFormSubmit);
        profileImageInput.addEventListener("change", changeProfilePicPreview);
        profilePicResetBtn.addEventListener("click", resetProfilePic);
        deleteProfileImageBtn.addEventListener("click", handleDeleteProfilePic);
    });

    $: hasMasterPassword = false;
    onMount(async () => {
        const masterPasswordForm = document.getElementById("master-password-form") as HTMLFormElement;
        const masterPasswordFormResetBtn = document.getElementById("master-password-form-reset-btn") as HTMLButtonElement;
        hasMasterPassword = await PromptMasterPassword();
        if (hasMasterPassword) {
            masterPasswordFormResetBtn.classList.remove("hidden");
        }

        const setupMasterPassword = async (masterPassword: string): Promise<void> => {
            if (masterPassword === "") {
                return;
            }

            try {
                const result = await swal.fire({
                    title: await translateText("Confirm Master Password"),
                    text: await translateText("Please enter your master password again as confirmation."),
                    input: "password",
                    inputAttributes: {
                        autocapitalize: "off",
                        autocorrect: "off",
                    },
                    showCancelButton: true,
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                    showLoaderOnConfirm: true,
                    cancelButtonText: await translateText("Cancel"),
                    confirmButtonText: await translateText("master_password_submit", $language, "Submit"),
                    preConfirm: async (password: string): Promise<void> => {
                        if (password === "") {
                            return Swal.showValidationMessage(
                                await translateText("Password cannot be empty"));
                        }
                        if (password !== masterPassword) {
                            return Swal.showValidationMessage(
                                await translateText("Entered password does not match your master password!"));
                        }
                        return;
                    },
                })
                if (!result.isConfirmed) {
                    return;
                }

                await SetMasterPassword(masterPassword);
                swal.fire({
                    title: await translateText("Success"),
                    text: await translateText("Master password has been updated."),
                    icon: "success",
                });
                hasMasterPassword = true;
                masterPasswordFormResetBtn.classList.remove("hidden");
            } catch (e) {
                console.error(e);
                if (e) {
                    LogError(e.toString());
                }
                swal.fire({
                    title: await translateText("Error"),
                    text: await translateText("An error occurred while setting the master password. Please try again later."),
                    icon: "error",
                });
            }
        };

        const changeMasterPassword = async (currentMasterPassword: string, newMasterPassword: string) => {
            if (currentMasterPassword === "" || newMasterPassword === "") {
                swal.fire({
                    title: await translateText("Error"),
                    text: await translateText("Please fill in the current and new master password fields."),
                    icon: "error",
                });
                return;
            }

            if (currentMasterPassword === newMasterPassword) {
                swal.fire({
                    title: await translateText("Error"),
                    text: await translateText("The new master password is the same as the current one."),
                    icon: "error",
                });
                return;
            }

            if (!await CheckMasterPassword(currentMasterPassword)) {
                swal.fire({
                    title: await translateText("Error"),
                    text: await translateText("The current master password is incorrect."),
                    icon: "error",
                });
                return;
            }

            const result = await swal.fire({
                title: await translateText("Confirm Master Password Change"),
                text: await translateText("Please enter your new master password again to confirm the change."),
                input: "password",
                inputAttributes: {
                    autocapitalize: "off",
                    autocorrect: "off",
                },
                showCancelButton: true,
                allowEscapeKey: false,
                allowOutsideClick: false,
                showLoaderOnConfirm: true,
                cancelButtonText: await translateText("Cancel"),
                confirmButtonText: await translateText("master_password_submit", $language, "Submit"),
                preConfirm: async (password: string): Promise<void> => {
                    if (password === "") {
                        return Swal.showValidationMessage(
                            await translateText("Password cannot be empty"));
                    }
                    if (password !== newMasterPassword) {
                        return Swal.showValidationMessage(
                            await translateText("Entered password does not match your new master password!"));
                    }
                    return;
                },
            })
            if (!result.isConfirmed) {
                return;
            }

            try {
                await ChangeMasterPassword(currentMasterPassword, newMasterPassword);
                swal.fire({
                    title: await translateText("Success"),
                    text: await translateText("Master password has been updated."),
                    icon: "success",
                });
            } catch (e) {
                console.error(e);
                if (e) {
                    LogError(e.toString());
                }
                swal.fire({
                    title: await translateText("Error"),
                    text: await translateText("An error occurred while setting the master password. Please try again later."),
                    icon: "error",
                });
            }
        };

        const handleMasterPasswordFormSubmit = async (e: Event): Promise<void> => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const formData = new FormData(form);
            const masterPassword = formData.get("master-password") as string;
            const currentMasterPassword = formData.get("current-master-password") as string;
            const newMasterPassword = formData.get("new-master-password") as string;

            if (!hasMasterPassword) {
                await setupMasterPassword(masterPassword);
                return;
            }
            await changeMasterPassword(currentMasterPassword, newMasterPassword);
        };

        const resetMasterPasswordForm = async (): Promise<void> => {
            const result = await invertedSwal.fire({
                title: await translateText("Remove Master Password?"),
                text: await translateText("All your sensitive data like your session cookies will be exposed! This is not recommended unless you are using your own device."),
                icon: "info",
                showCancelButton: true,
                cancelButtonText: await translateText("Cancel"),
            })
            if (!result.isConfirmed) {
                return;
            }

            await RemoveMasterPassword();
            hasMasterPassword = false;
            masterPasswordFormResetBtn.classList.add("hidden");
            swal.fire({
                title: await translateText("Master password removed"),
                text: await translateText("You have removed your master password and all your saved encrypted data has been decrypted."),
                icon: "success",
            });
        };

        masterPasswordForm.addEventListener("submit", handleMasterPasswordFormSubmit);
        masterPasswordFormResetBtn.addEventListener("click", resetMasterPasswordForm);
    });
</script>

<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <div class="mx-auto text-center">
        <img class="rounded-full w-32 h-32 border-4 mt-2 border-gray-200" id="profile-img-el" alt="user profile" src="{bufferGif}" />
        <button id="profile-pic-reset-btn" class="text-small hidden text-red-500 hover:text-red-600">
            {translate("Reset Image", "profile-pic-reset-btn", $language)}
        </button>
    </div>
    <form class="md:col-span-3" id="general-form">
        <div class="flex">
            <div class="w-full">
                <Label for="username" class="pb-2">
                    <Translate text="Username:" {language} />
                </Label>
                <Input name="username" id="username" />
            </div>
        </div>
        <div class="flex mt-4">
            <div class="w-full">
                <Label for="language">
                    <Translate text="Language:" {language} />
                </Label>
                <Select 
                    class="my-2" 
                    name="language" 
                    id="language" 
                    items={LANGUAGES} 
                    bind:value={lang} 
                />
            </div>
        </div>
        <div class="flex mt-4">
            <div class="w-full">
                <Label for="profile-image" class="pb-2">
                    <Translate text="Upload Profile Image:" {language} />
                </Label>
                <Fileupload name="profile-image" id="profile-image" class="mb-2" />
                <Helper>
                    <Translate text="PNG, JPG, GIF or WEBP." {language} />
                </Helper>
                <Input name="profile-image-path" id="profile-image-path" type="hidden" />
                <button id="delete-profile-image-btn" type="button" class="btn btn-danger mt-4 ms-3 float-end">
                    {translate("Reset", "delete-profile-image-btn", $language)}
                </button>
                <button type="submit" class="btn btn-success mt-4 float-end !me-0">
                    <Translate text="Save All" {language} />
                </button>
            </div>
        </div>
    </form>
    <form class="md:col-start-2 md:col-span-3" id="master-password-form">
        <Hr />
        {#if hasMasterPassword}
            <div class="flex">
                <div class="w-full" id="current-master-password-div">
                    <Label for="current-master-password" class="pb-2">
                        <Translate text="Current Master Password:" {language} />
                    </Label>
                    <PasswordToggle>
                        <Input name="current-master-password" id="current-master-password" type="password" />
                    </PasswordToggle>
                </div>
            </div>
            <div class="flex">
                <div class="mt-4 w-full" id="new-master-password-div">
                    <Label for="new-master-password" class="pb-2">
                        <Translate text="New Master Password:" {language} />
                    </Label>
                    <PasswordToggle>
                        <Input name="new-master-password" id="new-master-password" type="password" />
                    </PasswordToggle>
                </div>
            </div>
        {:else}
            <div class="flex">
                <div class="w-full">
                    <Label for="master-password" class="pb-2">
                        <Translate text="Master Password:" {language} />
                    </Label>
                    <PasswordToggle>
                        <Input name="master-password" id="master-password" type="password" />
                    </PasswordToggle>
                </div>
            </div>
        {/if}
        <div class="text-right mt-4">
            <button id="master-password-form-reset-btn" type="button" class="btn btn-danger hidden">
                {translate("Reset", "master-password-form-reset-btn", $language)}
            </button>
            <button type="submit" class="btn btn-success !me-0">
                <Translate text="Save" {language} />
            </button>
        </div>
    </form>
</div>
