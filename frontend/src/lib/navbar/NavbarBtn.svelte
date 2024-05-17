<script lang="ts">
    import { actions, logoImgSrc, navbarLogoSize } from "../../scripts/constants";
    import { actionTitleCase } from "../../scripts/utils/string";
    import { translate } from "../../scripts/language";
    import type { Writable } from "svelte/store";

    export let action: Writable<string>;
    export let language: Writable<string>;
    export let btnRole: string;

    const sideNavBarId = `${btnRole}-side-navbar`;
    const actionTitle = actionTitleCase(btnRole);
    $: actionMatches = $action === btnRole;
</script>

<button 
    on:click={() => {action.set(btnRole)}} 
    class="w-full flex items-center p-2 rounded-lg group {
        actionMatches ? 
        "bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white" : 
        "hover:bg-zinc-100 dark:hover:bg-zinc-700 text-zinc-500 transition duration-75 dark:text-zinc-400"
    }"
>
    {#if btnRole === actions.Home}
        <svg class="{navbarLogoSize}" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16"> 
            <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5z"/>
        </svg>
    {:else if btnRole === actions.Downloads}
        <svg class="flex-shrink-0 {navbarLogoSize}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" >
            <path d="M11 5C11 4.44772 11.4477 4 12 4C12.5523 4 13 4.44772 13 5V12.1578L16.2428 8.91501L17.657 10.3292L12.0001 15.9861L6.34326 10.3292L7.75748 8.91501L11 12.1575V5Z" fill="currentColor" />
            <path d="M4 14H6V18H18V14H20V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V14Z" fill="currentColor" />
        </svg>
    {:else}
        <img class="flex-shrink-0 {navbarLogoSize}" src="{logoImgSrc[btnRole]}" alt="{actionTitle} Logo">
    {/if}

    <span class="ms-3" id="{sideNavBarId}">{translate(actionTitle, sideNavBarId, $language)}</span>
</button>
