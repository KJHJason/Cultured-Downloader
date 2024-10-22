<script lang="ts">
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import Translate from "../common/Translate.svelte";

    interface Props {
        errors: string[];
    }

    let { errors }: Props = $props();
</script>

<Table hoverable={false} shadow={true}>
    <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
        <TableHeadCell>
            <Translate text="Errors" />
        </TableHeadCell>
    </TableHead>
    <TableBody tableBodyClass="divide-y">
        {#each errors as err}
            <TableBodyRow>
                <TableBodyCell>
                    <pre class="text-wrap text-sm">{err}</pre>
                </TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>