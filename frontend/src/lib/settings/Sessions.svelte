<script lang="ts">
    import Session from "./Session.svelte";
</script>

<div class="grid grid-cols-1">
    <div>
        <Session title="Fantia (_session_id)" elId="fantia-session" website="fantia" placeholder="96854bb23e733aa0d44211936a3e1f8a8185f6bdb50e04047a845824ade3c2d0" />
    </div>
    <div>
        <Session title="Pixiv Fanbox (FANBOXSESSID)" elId="pixiv-fanbox-session" website="fanbox" placeholder="12312345_rAkUgAK1cH4nBeSTwA1FuSEmmmAZsEgG" />
    </div>
    <div>
        <Session title="Pixiv Web (PHPSESSID)" elId="pixiv-session" website="pixiv" placeholder="54321234_rAkUgAK1cH4nBeSTwA1FuSEmmmAZSeGg" />
    </div>
    <div>
        <Session title="Kemono (session)" elId="kemono-session" website="kemono" placeholder="eyJfcGVybWFuZW50Ijp0cnVlLCJhY2NvdW50X2lkIjoicmFrdWdha2ktY2hhbiJ9.eJGV..." />
    </div>
</div>
