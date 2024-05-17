<script lang="ts">
    import { writable, type Writable } from "svelte/store";
    import { translate } from "../../scripts/language";
    import { generateRandomId } from "../../scripts/random";

    export let text: string;
    export let spanClass: string = "";
    export let language: Writable<string> = writable("");
    const elementId = generateRandomId();
</script>

<span class={spanClass} id={elementId}>{translate(text, elementId, $language)}</span>
