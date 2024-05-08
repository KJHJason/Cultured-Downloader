<script lang="ts">
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { Translate } from "../../scripts/language";

    export let errors: any;
</script>

<Table hoverable={false} shadow={true}>
    <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
        <TableHeadCell>{Translate("Errors")}</TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        <TableBodyRow>
            {#each errors as err}
                <TableBodyCell>
                    {err}
                </TableBodyCell>
            {/each}
        </TableBodyRow>
    </TableBody>
</Table>