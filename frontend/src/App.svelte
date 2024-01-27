<script lang="ts">
    import Swal from "sweetalert2";
    import { onMount, createEventDispatcher } from "svelte";
    import "./scripts/dark-mode";
    import { swal, actions, changeActionEventType, invertedSwal } from "./scripts/constants";
    import Navbar from "./lib/Navbar.svelte";
    import Home from "./lib/Home.svelte";
    import Fantia from "./lib/Fantia.svelte";
    import Pixiv from "./lib/Pixiv.svelte";
    import PixivFanbox from "./lib/PixivFanbox.svelte";
    import Kemono from "./lib/Kemono.svelte";
    import DownloadQueues from "./lib/DownloadQueues.svelte";
    import Settings from "./lib/Settings.svelte";
    import { PromptMasterPassword, CheckMasterPassword, ResetEncryptedFields } from "./scripts/wailsjs/go/app/App";

    let action: string = "home";
    const handleActionChange = (event: CustomEvent<string>): void => {
        switch (event.type) {
            case changeActionEventType:
                action = event.detail;
                break;
            default:
                throw new Error(`Unknown event type: ${event.type}`);
        }
    };

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
            preConfirm: async (password): Promise<void> => {
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
                text: "You have entered the correct password",
            });
            return;
        } 

        invertedSwal.fire({
            showCancelButton: true,
            allowEscapeKey: false,
            allowOutsideClick: false,
            icon: "info",
            title: "Remove master password?",
            text: "All your saved encrypted config data will be lost",
            confirmButtonText: "Remove",
            cancelButtonText: "Back",
        }).then(async (result): Promise<void> => {
            if (result.isConfirmed) {
                await ResetEncryptedFields();
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
        await checkMasterPassword();
    });
</script>

<Navbar action={action} on:changeAction={handleActionChange}/>

<main class="p-4">
    <div class="mt-14">
        <Settings />
        <!-- {#if action === actions.Home}
            <Home/>
        {:else if action === actions.Fantia}
            <Fantia/>
        {:else if action === actions.Pixiv}
            <Pixiv/>
        {:else if action === actions.PixivFanbox}
            <PixivFanbox/>
        {:else if action === actions.Kemono}
            <Kemono/>
        {:else if action === actions.Downloads}
            <DownloadQueues/>
        {:else if action == actions.Settings}
            <Settings />
        {:else}
            <p>Not implemented yet</p>
        {/if} -->
    </div>
</main>
