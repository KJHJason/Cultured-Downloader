<script lang="ts">
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from "flowbite-svelte";
    import { BrowserOpenURL } from "../scripts/wailsjs/runtime/runtime";
    import loadingImg from "../assets/images/bocchi-loading.gif";
</script>

<div class="container mx-auto">
    <h2 class="mb-3">Download Queues</h2>
    <Table hoverable={true} shadow={true}>
        <TableHead theadClass="dark:!bg-gray-900 !bg-gray-200">
            <TableHeadCell>Thumbnail</TableHeadCell>
            <TableHeadCell>Title</TableHeadCell>
            <TableHeadCell>Progress</TableHeadCell>
            <TableHeadCell>Actions</TableHeadCell>
        </TableHead>
        <TableBody tableBodyClass="divide-y">
            <TableBodyRow>
                <TableBodyCell>
                    <img class="object-cover h-auto w-14 rounded" src={loadingImg} alt="post-thumbnail">
                </TableBodyCell>
                <TableBodyCell class="whitespace-normal">
                    <button on:click={() => BrowserOpenURL("https://fantia.jp")} class="btn-link break-words max-w-48 text-left">らくがきちゃん</button>
                </TableBodyCell>
                <TableBodyCell>
                    <div class="flex justify-between mb-1">
                        <span class="text-base font-medium text-blue-700 dark:text-white">Downloading...</span>
                        <span class="text-sm font-medium text-blue-700 dark:text-white">45%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                        <div class="bg-blue-600 h-2.5 rounded-full progress-bar" style="width: 45%"></div>
                    </div>
                </TableBodyCell>
                <TableBodyCell>
                    <!-- TODO: add download speed and eta info for each item to be downloaded on a modal -->
                    <button class="btn btn-info">View Details</button>
                    <button class="btn btn-danger">Cancel</button>
                </TableBodyCell>
            </TableBodyRow>
        </TableBody>
    </Table>
</div>
