<script lang="ts">
    import Swal from "sweetalert2";
    import { onDestroy, onMount } from "svelte";
    import { writable } from "svelte/store";
    import { swal, actions, invertedSwal } from "./scripts/constants";
    import { PromptMasterPassword, CheckMasterPassword, RemoveMasterPassword, GetUsername, GetLanguage } from "./scripts/wailsjs/go/app/App";
    import { LogError } from "./scripts/wailsjs/runtime/runtime";
    import { EN, translate, ChangeCachedLanguage, translateText } from "./scripts/language";

    import Navbar from "./lib/Navbar.svelte";
    import Home from "./lib/Home.svelte";
    import Fantia from "./lib/Fantia.svelte";
    import Pixiv from "./lib/Pixiv.svelte";
    import PixivFanbox from "./lib/PixivFanbox.svelte";
    import Kemono from "./lib/Kemono.svelte";
    import DownloadQueues from "./lib/DownloadQueues.svelte";
    import Settings from "./lib/Settings.svelte";

    const triggerSwalError = async (message: string): Promise<void> => {
        swal.fire({
            title: await translateText("Unexpected error"),
            text: message,
            icon: "error",
        });
    };
    window.onerror = (event: Event | string, source?: string, lineno?: number, colno?: number, error?: Error): void => {
        const errorMsg = event.toString();
        if (errorMsg.includes("ResizeObserver loop completed with undelivered notifications.")) {
            return;
        }

        console.error(errorMsg, source, lineno, colno, error);
        LogError(`${errorMsg} at ${source}:${lineno}:${colno}`);
        triggerSwalError(errorMsg);
    };
    window.addEventListener("error", (event: Event | string, source?: string, lineno?: number, colno?: number, error?: Error): void => {
        const errorMsg = event.toString();
        if (errorMsg === "[object ErrorEvent]") {
            return;
        }

        console.error(errorMsg, source, lineno, colno, error);
        LogError(`${errorMsg} at ${source}:${lineno}:${colno}`);
        triggerSwalError(errorMsg);
    });
    window.addEventListener("unhandledrejection", async (event: PromiseRejectionEvent): Promise<void> => {
        const errorMsg = event.reason ? event.reason.toString() : await translateText("Unknown error");
        console.error(errorMsg);
        LogError(errorMsg);
        triggerSwalError(errorMsg);
    });

    let lastSavedUpdateStr: Record<string, string> = $state({});
    const username = writable("");
    const action = writable(actions.Home);
    const language = writable(EN);
    const unsubscribeLanguage = language.subscribe((value: string): void => {
        ChangeCachedLanguage(value);
    });

    const checkMasterPassword = async (): Promise<void> => {
        if (!await PromptMasterPassword()) {
            return;
        }

        const result = await swal.fire({
            title: await translateText("Enter your master password"),
            input: "password",
            inputAttributes: {
                autocapitalize: "off",
                autocorrect: "off",
            },
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            showLoaderOnConfirm: true,
            cancelButtonText: await translateText("Remove"),
            confirmButtonText: await translateText("Submit"),
            preConfirm: async (password: string): Promise<void> => {
                if (password === "") {
                    return Swal.showValidationMessage(
                        await translateText("Password cannot be empty"));
                }

                const result = await CheckMasterPassword(password);
                if (!result) {
                    return Swal.showValidationMessage(
                        await translateText("Incorrect password"));
                }
                return;
            },
        });

        if (result.isConfirmed) {
            swal.fire({
                icon: "success",
                title: await translateText("Correct password"),
                text: await translateText("You have entered the correct password."),
            });
            return;
        } 

        invertedSwal.fire({
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            icon: "info",
            title: await translateText("Remove master password?"),
            text: await translateText("All your sensitive data like your session cookies will be exposed! This is not recommended unless you are using your own device."),
            confirmButtonText: await translateText("Remove"),
            cancelButtonText: await translateText("Back"),
        }).then(async (result): Promise<void> => {
            if (result.isConfirmed) {
                await RemoveMasterPassword();
                swal.fire({
                    icon: "success",
                    title: await translateText("Master password removed"),
                    text: await translateText("You have removed your master password and all your saved encrypted data has been decrypted."),
                });
            } else {
                checkMasterPassword();
            }
        });
    };

    onMount(async () => {
        const lang = await GetLanguage();
        language.set(lang);

        username.set(await GetUsername() || "User");
        await checkMasterPassword();
    });

    onDestroy(() => {
        unsubscribeLanguage();
    });
</script>

<Navbar {username} {action} {language} />

{#if $action === actions.Home}
    <Home {action} {username} />
{:else}
    <main class="p-4">
        <div class="mt-14">
            {#if $action === actions.Fantia}
                <Fantia />
            {:else if $action === actions.Pixiv}
                <Pixiv />
            {:else if $action === actions.PixivFanbox}
                <PixivFanbox />
            {:else if $action === actions.Kemono}
                <Kemono />
            {:else if $action === actions.Downloads}
                <DownloadQueues {action} />
            {:else if $action === actions.Settings}
                <Settings {username} bind:lastSavedUpdateStr {language} />
            {:else if $action !== actions.Home}
                <p id="not-implemented-yet">{translate("Not implemented yet", "not-implemented-yet")}</p>
            {/if}
        </div>
    </main>
{/if}
