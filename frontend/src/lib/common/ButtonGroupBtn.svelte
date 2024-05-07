<script lang="ts">
    export let elId: string;
    export let btnClass = "";
    export let clickFn: () => void;
</script>

<button type="button" on:click={clickFn} id="{elId}" class="{btnClass} p-2 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 dark:border-gray-600 rounded-r-lg rounded-l-none mt-2 border-s-0 border">
    <slot />
</button>
