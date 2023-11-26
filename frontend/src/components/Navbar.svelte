<script>
    import { onMount } from "svelte";
    import { GetName } from "../lib/wailsjs/go/main/App.js";
    import cdLogo from "../assets/images/logos/cultured-downloader-logo.png";
    import fantiaLogo from "../assets/images/logos/fantia-logo.png";
    import pixivFanboxLogo from "../assets/images/logos/pixiv-fanbox-logo.png";
    import pixivLogo from "../assets/images/logos/pixiv-logo.png";
    import kemonoLogo from "../assets/images/logos/kemono-logo.png";

    const logoSizeClass = "h-8 w-8";
    let name = "";
    onMount(async () => {
        name = await GetName();
    });

    export let action = "";
    export let actions = {};
    const changeAction = (newAction) => {
        action = newAction;
    };
</script>

<nav class="fixed top-0 z-50 w-full bg-white border-b border-zinc-200 dark:bg-zinc-800 dark:border-zinc-700">
    <div class="px-3 py-3 lg:px-5 lg:pl-3">
        <div class="flex items-center justify-between">
            <div class="flex items-center justify-start rtl:justify-end">
                <button data-drawer-target="logo-sidebar" data-drawer-toggle="logo-sidebar" aria-controls="logo-sidebar" type="button" class="inline-flex items-center p-2 text-sm text-zinc-500 rounded-lg sm:hidden hover:bg-zinc-100 focus:outline-none focus:ring-2 focus:ring-zinc-200 dark:text-zinc-400 dark:hover:bg-zinc-700 dark:focus:ring-zinc-600">
                    <span class="sr-only">Open sidebar</span>
                    <svg class="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path clip-rule="evenodd" fill-rule="evenodd" d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
                    </svg>
                </button>
                <div class="flex ms-2 md:me-24">
                    <img src="{cdLogo}" class="h-8 me-3" alt="Cultured Downloader Logo" />
                    <span class="self-center text-xl font-semibold sm:text-2xl whitespace-nowrap dark:text-white">Cultured Downloader</span>
                </div>
            </div>
            <div class="flex items-center">
                <div class="flex items-center ms-3">
                    <div>
                        <button type="button" class="flex text-sm bg-zinc-800 rounded-full focus:ring-4 focus:ring-zinc-300 dark:focus:ring-zinc-600" aria-expanded="false" data-dropdown-toggle="dropdown-user">
                            <span class="sr-only">Open user menu</span>
                            <img class="w-8 h-8 rounded-full" src="/profile.png" alt="" />
                        </button>
                    </div>
                    <div class="z-50 hidden my-4 text-base list-none bg-white divide-y divide-zinc-100 rounded shadow dark:bg-zinc-700 dark:divide-zinc-600" id="dropdown-user">
                        <div class="px-4 py-3" role="none">
                            <p class="text-sm text-zinc-900 dark:text-white" role="none"> {name} </p>
                            <p class="text-sm font-medium text-zinc-900 truncate dark:text-zinc-300" role="none"> neil.sims@flowbite.com </p>
                        </div>
                        <ul class="py-1" role="none">
                            <li>
                                <a href="/" class="flex justify-center items-center px-4 py-2 text-sm text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-600 dark:hover:text-white" role="menuitem">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
                                    <span class="flex-1 ms-2 text-left whitespace-nowrap">Settings</span>
                                </a>
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
<aside id="logo-sidebar" class="fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full bg-white border-r border-zinc-200 sm:translate-x-0 dark:bg-zinc-800 dark:border-zinc-700" aria-label="Sidebar">
    <div class="h-full px-3 pb-4 overflow-y-auto bg-white dark:bg-zinc-800">
        <ul class="space-y-2 font-medium">
            <li>
                <button on:click={() => changeAction(actions.Home)} class="w-full flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group">
                    <svg class="{logoSizeClass} text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white"  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"> <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5z"/></svg>
                    <span class="ms-3">Home</span>
                </button>
            </li>
            <li>
                <button on:click={() => changeAction(actions.Fantia)} class="w-full flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group">
                    <img class="flex-shrink-0 {logoSizeClass}" src="{fantiaLogo}" alt="Fantia Logo">
                    <span class="flex-1 text-left ms-3 whitespace-nowrap text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white">
                        Fantia
                    </span>
                </button>
            </li>
            <li>
                <button on:click={() => changeAction(actions.Pixiv)} class="w-full flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group">
                    <img class="flex-shrink-0 {logoSizeClass}" src="{pixivLogo}" alt="Pixiv Logo">
                    <span class="flex-1 text-left ms-3 whitespace-nowrap text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white">
                        Pixiv
                    </span>
                    <!-- <span class="inline-flex items-center justify-center w-3 h-3 p-3 ms-3 text-sm font-medium text-blue-800 bg-blue-100 rounded-full dark:bg-blue-900 dark:text-blue-300">3</span> -->
                </button>
            </li>
            <li>
                <button on:click={() => changeAction(actions.PixivFanbox)} class="w-full flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group">
                    <img class="flex-shrink-0 {logoSizeClass}" src="{pixivFanboxLogo}" alt="Pixiv Fanbox Logo">
                    <span class="flex-1 text-left ms-3 whitespace-nowrap text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white">
                        Pixiv Fanbox
                    </span>
                </button>
            </li>
            <li>
                <button on:click={() => changeAction(actions.Kemono)} class="w-full flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group">
                    <img class="flex-shrink-0 {logoSizeClass}" src="{kemonoLogo}" alt="Kemono Logo">
                    <span class="flex-1 text-left ms-3 whitespace-nowrap text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white">
                        Kemono Party
                    </span>
                </button>
            </li>
            <li>
                <button on:click={() => changeAction(actions.Downloads)} class="w-full flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group">
                    <svg class="flex-shrink-0 {logoSizeClass} text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" ><path d="M11 5C11 4.44772 11.4477 4 12 4C12.5523 4 13 4.44772 13 5V12.1578L16.2428 8.91501L17.657 10.3292L12.0001 15.9861L6.34326 10.3292L7.75748 8.91501L11 12.1575V5Z" fill="currentColor" /> <path d="M4 14H6V18H18V14H20V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V14Z" fill="currentColor" /> </svg>
                    <span class="flex-1 text-left ms-3 whitespace-nowrap text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white">
                        Download Queues
                    </span>
                </button>
                <!-- <button id="theme-toggle" type="button" class="flex items-center p-2 text-zinc-900 rounded-lg dark:text-white hover:bg-zinc-100 dark:hover:bg-zinc-700 group w-full">
                    <div class="flex-shrink-0 {logoSizeClass} text-zinc-500 transition duration-75 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white">
                        <svg id="theme-toggle-dark-icon" class="hidden" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                        <svg id="theme-toggle-light-icon" class="hidden" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
                    </div>
                    <span class="flex-1 ms-3 text-left whitespace-nowrap" id="theme-toggle-text"></span>
                </button> -->
            </li>
        </ul>
    </div>
</aside>
