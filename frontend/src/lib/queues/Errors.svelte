<script lang="ts">
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import Translate from "../common/Translate.svelte";

    export let errors: any;
</script>

<Table hoverable={false} shadow={true}>
    <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
        <TableHeadCell>
            <Translate text="Errors" />
        </TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        <TableBodyRow>
            {#each errors as err}
                <TableBodyCell>
                    <pre class="text-wrap text-sm">{err}</pre>
                </TableBodyCell>
            {/each}
        </TableBodyRow>
    </TableBody>
</Table>