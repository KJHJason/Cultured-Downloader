<script lang="ts">
    import Swal from "sweetalert2";

    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import { Spinner } from "flowbite-svelte";
    import { swal, actions, invertedSwal } from "./scripts/constants";
    import { PromptMasterPassword, CheckMasterPassword, RemoveMasterPassword, GetUsername } from "./scripts/wailsjs/go/app/App";
    import { InitialiseLanguage } from "./scripts/language";

    import Navbar from "./lib/Navbar.svelte";
    import Home from "./lib/Home.svelte";
    import Fantia from "./lib/Fantia.svelte";
    import Pixiv from "./lib/Pixiv.svelte";
    import PixivFanbox from "./lib/PixivFanbox.svelte";
    import Kemono from "./lib/Kemono.svelte";
    import DownloadQueues from "./lib/DownloadQueues.svelte";
    import Settings from "./lib/Settings.svelte";

    const triggerSwalError = (message: string): void => {
        swal.fire({
            title: "Unexpected error",
            text: message,
            icon: "error",
        });
    };
    window.onerror = (event: Event | string, source?: string, lineno?: number, colno?: number, error?: Error): void => {
        const errorMsg = event.toString();
        console.error(errorMsg, source, lineno, colno, error);
        triggerSwalError(errorMsg);
    };
    window.addEventListener("error", (event: Event | string, source?: string, lineno?: number, colno?: number, error?: Error): void => {
        const errorMsg = event.toString();
        console.error(errorMsg, source, lineno, colno, error);
        triggerSwalError(errorMsg);
    });
    window.addEventListener("unhandledrejection", (event: PromiseRejectionEvent): void => {
        const errorMsg = event.reason ? event.reason.toString() : "Unknown error";
        console.error(errorMsg);
        triggerSwalError(errorMsg);
    });

    $: username = "";
    $: lastSavedUpdateStr = "";
    const action = writable(actions.Home);

    const checkMasterPassword = async (): Promise<void> => {
        if (!await PromptMasterPassword()) {
            return;
        }

        const result = await swal.fire({
            title: "Enter your master password",
            input: "password",
            inputAttributes: {
                autocapitalize: "off",
                autocorrect: "off",
            },
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            showLoaderOnConfirm: true,
            cancelButtonText: "Remove",
            confirmButtonText: "Submit",
            preConfirm: async (password: string): Promise<void> => {
                if (password === "") {
                    return Swal.showValidationMessage("Password cannot be empty");
                }

                const result = await CheckMasterPassword(password);
                if (!result) {
                    return Swal.showValidationMessage("Incorrect password");
                }
                return;
            },
        });

        if (result.isConfirmed) {
            swal.fire({
                icon: "success",
                title: "Correct password",
                text: "You have entered the correct password.",
            });
            return;
        } 

        invertedSwal.fire({
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            icon: "info",
            title: "Remove master password?",
            text: "All your saved encrypted config data will be lost.",
            confirmButtonText: "Remove",
            cancelButtonText: "Back",
        }).then(async (result): Promise<void> => {
            if (result.isConfirmed) {
                await RemoveMasterPassword();
                swal.fire({
                    icon: "success",
                    title: "Master password removed",
                    text: "You have removed your master password and all your saved encrypted config data have been removed.",
                });
            } else {
                checkMasterPassword();
            }
        });
    };
    onMount(async () => {
        username = await GetUsername();
        await checkMasterPassword();
    });
</script>

<Navbar bind:username {action} />

<main class="p-4">
    <div class="mt-14">
        {#await InitialiseLanguage()}
            <Spinner color="blue" />
        {:then}
            <!-- <Settings username={username} handleActionChange={handleActionChange} /> -->
            <!-- <Fantia /> -->
            <!-- <Pixiv /> -->
            <!-- <DownloadQueues bind:action /> -->
            {#if $action === actions.Home}
                <Home/>
            {:else if $action === actions.Fantia}
                <Fantia/>
            {:else if $action === actions.Pixiv}
                <Pixiv/>
            {:else if $action === actions.PixivFanbox}
                <PixivFanbox/>
            {:else if $action === actions.Kemono}
                <Kemono/>
            {:else if $action === actions.Downloads}
                <DownloadQueues {action} />
            {:else if $action === actions.Settings}
                <Settings bind:username bind:lastSavedUpdateStr />
            {:else}
                <p>Not implemented yet</p>
            {/if}
        {:catch error}
            <p>Unexpected error!: {error.message}</p>
        {/await}
    </div>
</main>
