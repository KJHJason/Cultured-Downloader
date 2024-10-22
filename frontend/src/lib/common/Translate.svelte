<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { translate } from "../../scripts/language";
    import { generateRandomId } from "../../scripts/utils/random";

    interface Props {
        text: string;
        fallback?: string;
        spanClass?: string;
        language?: Writable<string>;
    }

    let {
        text,
        fallback = "",
        spanClass = "",
        language = writable(""),
    }: Props = $props();

    const elementId = generateRandomId();
</script>

<span class={spanClass} id={elementId}>{translate(text, elementId, $language, fallback)}</span>
