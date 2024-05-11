<script lang="ts">
    import { onDestroy } from "svelte";
    import { swal } from "../../scripts/constants";

    swal.fire({
        title: "",
        text: "Please wait for the program to load...",
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        showConfirmButton: false,
        willOpen: () => {
            swal.showLoading();
        }
    });

    onDestroy(() => {
        swal.close();
    });
</script>
