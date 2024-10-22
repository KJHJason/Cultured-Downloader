<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { translate } from "../../scripts/language";
    import { generateRandomId } from "../../scripts/utils/random";

    interface Props {
        text: string;
        fallback?: string;
        spanClass?: string;
        language?: Writable<string>;
        otherAttributes?: Record<string, string>;
    }

    let {
        text,
        fallback = "",
        spanClass = "",
        language = writable(""),
        otherAttributes = {}
    }: Props = $props();

    const elementId = generateRandomId();
</script>

<span class={spanClass} id={elementId} {...otherAttributes}>{translate(text, elementId, $language, fallback)}</span>
