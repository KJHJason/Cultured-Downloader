<script lang="ts">
    import { createEventDispatcher, onMount } from "svelte";
    import { actions, changeActionEventType } from "../scripts/constants";
    import cdLogo from "../assets/images/logos/cultured-downloader-logo.png";
    import bufferGif from "../assets/images/buffer.gif";
    import NavbarBtn from "./navbar/NavbarBtn.svelte";
    import { InitialiseDarkModeConfig } from "../scripts/dark-mode";

    export let action: string;
    export let username: string;

    onMount(async () => {
        await InitialiseDarkModeConfig();
    });

    const dispatcher = createEventDispatcher();
    const changeAction = (newAction: string): void => {
        action = newAction;
        dispatcher(changeActionEventType, action);
    };
</script>

<nav class="fixed top-0 z-50 w-full border-b bg-item">
    <div class="px-3 py-3 lg:px-5 lg:pl-3">
        <div class="flex items-center justify-between">
            <div class="flex items-center justify-start rtl:justify-end">
                <button data-drawer-target="logo-sidebar" data-drawer-toggle="logo-sidebar" aria-controls="logo-sidebar" type="button" class="inline-flex items-center p-2 text-sm text-zinc-500 rounded-lg hover:bg-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-200 dark:text-zinc-400 dark:hover:bg-zinc-700 dark:focus:ring-zinc-600">
                    <span class="sr-only">Open sidebar</span>
                    <svg class="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path clip-rule="evenodd" fill-rule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
                    </svg>
                </button>
                <div class="flex ms-2 md:me-24">
                    <img src="{cdLogo}" class="h-8 me-3" alt="Cultured Downloader Logo" />
                    <span class="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap text-main">Cultured Downloader</span>
                </div>
            </div>
            <div class="flex items-center">
                <div class="flex items-center ms-3">
                    <div>
                        <button type="button" class="flex text-sm bg-zinc-800 rounded-full focus:ring-4 focus:ring-zinc-300 dark:focus:ring-zinc-600" aria-expanded="false" data-dropdown-toggle="dropdown-user">
                            <span class="sr-only">Open user menu</span>
                            <img class="w-8 h-8 rounded-full border-2 border-gray-200" src="{bufferGif}" alt="user profile" id="navbar-user-profile" />
                        </button>
                    </div>
                    <div class="z-50 hidden my-4 text-base list-none bg-white divide-y divide-zinc-200 rounded shadow dark:bg-zinc-800 dark:divide-zinc-600 outline-zinc-200 outline-1 dark:outline-zinc-600 outline" id="dropdown-user">
                        <div class="px-4 py-3" role="none">
                            <p class="text-sm text-zinc-900 dark:text-white" role="none"> {username} </p>
                            <p class="text-sm font-medium text-zinc-900 truncate dark:text-zinc-300" role="none"> {username}@cd.kjhjason.com </p>
                        </div>
                        <ul class="p-1" role="none">
                            <li>
                                <button on:click={() => changeAction(actions.Settings)} class="flex justify-center items-center px-4 py-2 text-sm text-zinc-700 hover:bg-zinc-100 dark:text-zinc-200 dark:hover:bg-zinc-600 dark:hover:text-white group w-full" role="menuitem">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                                    <span class="flex-1 ms-2 text-left whitespace-nowrap">Settings</span>
                                </button>
                            </li>
                            <li>
                                <button id="theme-toggle" type="button" class="flex justify-center items-center px-4 py-2 text-sm text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-600 dark:hover:text-white group w-full"  role="menuitem">
                                    <div class="flex-shrink-0 h-4 w-4">
                                        <svg id="theme-toggle-dark-icon" class="hidden" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                                        <svg id="theme-toggle-light-icon" class="hidden" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
                                    </div>
                                    <span class="flex-1 ms-2 text-left whitespace-nowrap" id="theme-toggle-text"></span>
                                </button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</nav>
<aside id="logo-sidebar" class="fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full bg-item border-r" aria-label="Sidebar">
    <div class="h-full px-3 pb-4 overflow-y-auto bg-white dark:bg-zinc-800">
        <ul class="space-y-2 font-medium">
            <li>
                <NavbarBtn btnRole={actions.Home} action={action} changeAction={changeAction} />
            </li>
            <li>
                <NavbarBtn btnRole={actions.Fantia} action={action} changeAction={changeAction} />
            </li>
            <li>
                <NavbarBtn btnRole={actions.Pixiv} action={action} changeAction={changeAction} />
            </li>
            <li>
                <NavbarBtn btnRole={actions.PixivFanbox} action={action} changeAction={changeAction} />
            </li>
            <li>
                <NavbarBtn btnRole={actions.Kemono} action={action} changeAction={changeAction} />
            </li>
            <li>
                <NavbarBtn btnRole={actions.Downloads} action={action} changeAction={changeAction} />
            </li>
        </ul>
    </div>
</aside>
