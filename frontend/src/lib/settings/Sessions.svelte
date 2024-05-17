<script lang="ts">
    import Session from "./Session.svelte";
    import { translateText } from "../../scripts/language";
    import { onMount } from "svelte";

    $: translatedDeleteBtnText = "";
    $: translatedSaveBtnText = "";
    $: translatedUploadBtnText = "";
    $: translatedPixivOauthText = "";
    $: translatedSavedSessionCookieText = "";
    $: translatedDeletedSessionCookieText = "";
    $: translatedErrText = "";
    onMount(async () => {
        translatedDeleteBtnText = await translateText("Delete");
        translatedSaveBtnText = await translateText("Save");
        translatedUploadBtnText = await translateText("Upload Netscape/Mozilla generated cookie file");
        translatedPixivOauthText = await translateText("If you have saved an OAuth Refresh Token for Pixiv in the Advanced tab, you can ignore/delete this field as the program will use the token instead.");
        translatedSavedSessionCookieText = await translateText("Session cookie saved successfully");
        translatedDeletedSessionCookieText = await translateText("Saved session cookie deleted successfully");
        translatedErrText = await translateText("Error");
    });
</script>

<div class="grid grid-cols-1">
    <div>
        <Session
            title="Fantia (_session_id)"
            elId="fantia-session"
            website="fantia"
            placeholder="96854bb23e733aa0d44211936a3e1f8a8185f6bdb50e04047a845824ade3c2d0"
            {translatedDeleteBtnText}
            {translatedSaveBtnText}
            {translatedUploadBtnText}
            {translatedPixivOauthText}
            {translatedDeletedSessionCookieText}
            {translatedSavedSessionCookieText}
            {translatedErrText}
        />
    </div>
    <div>
        <Session
            title="Pixiv Fanbox (FANBOXSESSID)"
            elId="pixiv-fanbox-session"
            website="fanbox"
            placeholder="12312345_rAkUgAK1cH4nBeSTwA1FuSEmmmAZsEgG"
            {translatedDeleteBtnText}
            {translatedSaveBtnText}
            {translatedUploadBtnText}
            {translatedPixivOauthText}
            {translatedDeletedSessionCookieText}
            {translatedSavedSessionCookieText}
            {translatedErrText}
        />
    </div>
    <div>
        <Session
            title="Pixiv Web (PHPSESSID)"
            elId="pixiv-session"
            website="pixiv"
            placeholder="54321234_rAkUgAK1cH4nBeSTwA1FuSEmmmAZSeGg"
            {translatedDeleteBtnText}
            {translatedSaveBtnText}
            {translatedUploadBtnText}
            {translatedPixivOauthText}
            {translatedDeletedSessionCookieText}
            {translatedSavedSessionCookieText}
            {translatedErrText}
        />
    </div>
    <div>
        <Session
            title="Kemono (session)"
            elId="kemono-session"
            website="kemono"
            placeholder="eyJfcGVybWFuZW50Ijp0cnVlLCJhY2NvdW50X2lkIjoicmFrdWdha2ktY2hhbiJ9.eJGV..."
            {translatedDeleteBtnText}
            {translatedSaveBtnText}
            {translatedUploadBtnText}
            {translatedPixivOauthText}
            {translatedDeletedSessionCookieText}
            {translatedSavedSessionCookieText}
            {translatedErrText}
        />
    </div>
</div>
