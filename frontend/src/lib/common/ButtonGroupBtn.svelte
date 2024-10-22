<script lang="ts">
    interface Props {
        elId: string;
        btnClass?: string;
        clickFn: () => void;
        children?: import('svelte').Snippet;
    }

    let {
        elId,
        btnClass = "",
        clickFn,
        children
    }: Props = $props();
</script>

<button type="button" onclick={clickFn} id="{elId}" class="{btnClass} p-2 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 dark:border-gray-600 rounded-r-lg rounded-l-none mt-2 border-s-0 border">
    {@render children?.()}
</button>
