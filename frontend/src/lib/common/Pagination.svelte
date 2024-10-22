<script lang="ts">
    import { type Writable, writable } from "svelte/store";
    import { translate } from "../../scripts/language";
    import Translate from "./Translate.svelte";
    import { onDestroy } from "svelte";

    interface Props {
        pageNum?: Writable<number>;
        rowsPerPage: number;
        elements: Writable<any[]>;
        paginatedEl: Writable<any[]>;
        showInfoIfNoEntry?: boolean;
    }

    let {
        pageNum = writable(1),
        rowsPerPage,
        elements,
        paginatedEl,
        showInfoIfNoEntry = true
    }: Props = $props();

    paginatedEl.set($elements.slice(0, rowsPerPage));
    let maxPages = $state(Math.ceil($elements.length / rowsPerPage));

    const onNext = () => setToPageNum($pageNum + 1);
    const onPrev = () => setToPageNum($pageNum - 1);
    const setToPageNum = (num: number) => {
        if (num < 1 || num > maxPages) {
            return;
        }

        pageNum.set(num);
        const startIndex = ($pageNum - 1) * rowsPerPage;
        const endIndex = $pageNum * rowsPerPage;
        paginatedEl.set($elements.slice(startIndex, endIndex));
    };

    const getHoverBtnClass = (disabled: boolean): string => {
        return disabled ? "" : "hover:text-gray-700 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700";
    };

    const getBtnTextClass = (disabled: boolean): string => {
        return disabled ? "text-gray-500 dark:text-gray-400" : "btn-text-link";
    };

    let prevBtnDisabled = $derived($pageNum === 1);
    let nextBtnDisabled = $derived($pageNum === maxPages);

    let minElIdx = $derived(($pageNum - 1) * rowsPerPage + 1);
    let maxElIdx = $derived(Math.min($pageNum * rowsPerPage, $elements.length));

    interface btnsToAddInfo {
        i:        number;
        isBuffer: boolean;
    }

    const getBtnsToAdd = (pageNum: number): btnsToAddInfo[] => {
        const btnsToAddSlice: btnsToAddInfo[] = [];
        if (maxPages <= 7) {
            for (let i = 1; i <= maxPages; i++) {
                btnsToAddSlice.push({ i, isBuffer: false });
            }
            return btnsToAddSlice;
        }

        let btnsToAdd: number;
        const nearToLowest = pageNum < 3 && maxPages > 3;
        const nearToHighest = pageNum > maxPages - 2 && maxPages > 3;
        if (nearToLowest) {
            btnsToAdd = 5 - pageNum;
        } else if (nearToHighest) {
            btnsToAdd = 5 - 1 - (maxPages - pageNum);
        } else {
            btnsToAdd = 2;
        }

        let lowerBound = pageNum - btnsToAdd;
        if (lowerBound <= 2) {
            // In the event that the lower bound is 
            // less than or equal to 2, we will start from 1
            lowerBound = 1;
        }

        // Note: lower bound will always be one when current page is < 3
        const addFirstPage = lowerBound != 1; 
        if (addFirstPage) {
            btnsToAddSlice.push({ i: 1, isBuffer: false });
            btnsToAddSlice.push({ i: -1, isBuffer: true });
        }

        let lastPageAdded: number = 0;
        const nBtnsToAdd = pageNum + btnsToAdd;
        for (let i = lowerBound; i <= maxPages && i <= nBtnsToAdd; i++) {
            btnsToAddSlice.push({ i, isBuffer: false });
            lastPageAdded = i;
        }

        if (lastPageAdded < maxPages) {
            if (lastPageAdded + 1 != maxPages) {
                btnsToAddSlice.push({ i: -1, isBuffer: true });
            }
            btnsToAddSlice.push({ i: maxPages, isBuffer: false });
        }
        return btnsToAddSlice;
    };

    let btnsToAdd: btnsToAddInfo[] = $state([]);
    const unsubscribeElChange = elements.subscribe((newElements) => {
        maxPages = Math.ceil(newElements.length / rowsPerPage);
        btnsToAdd = getBtnsToAdd($pageNum);
        setToPageNum($pageNum);
    });
    onDestroy(() => {
        unsubscribeElChange()
    });
</script>

{#if $elements.length === 0 && showInfoIfNoEntry}
    <p class="text-center text-gray-500 dark:text-gray-400" id="no-entries-msg">{translate("No entries to show.", "no-entries-msg")}</p>
{:else if $elements.length >= 1}
    <nav aria-label="Paginated Element Page Number" class="flex flex-col items-center">
        <span class="text-sm text-gray-700 dark:text-gray-400">
            <Translate text="Showing" />
            <span class="font-semibold text-gray-900 dark:text-white">{minElIdx}</span>
            <Translate text="to" />
            <span class="font-semibold text-gray-900 dark:text-white">{maxElIdx}</span>
            <Translate text="of" />
            <span class="font-semibold text-gray-900 dark:text-white">{$elements.length}</span>
            <Translate text="Entries" />
        </span>
        <ul class="inline-flex mt-2 xs:mt-0 -space-x-px h-10 text-base">
            <li>
                <button type="button" onclick={onPrev} class="flex items-center justify-center px-4 h-10 ms-0 leading-tight bg-white border border-e-0 border-gray-300 rounded-s-lg dark:bg-gray-800 dark:border-gray-700 {getHoverBtnClass(prevBtnDisabled)} {getBtnTextClass(prevBtnDisabled)}" disabled={prevBtnDisabled}>
                    <Translate spanClass="sr-only" text="Previous" />
                    <svg class="w-3 h-3 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 1 1 5l4 4"/>
                    </svg>
                </button>
            </li>
            {#each btnsToAdd as { i, isBuffer }}
                {#if isBuffer}
                    <button type="button" class="flex items-center justify-center px-4 h-10 leading-tight bg-white border border-gray-300 dark:bg-gray-800 dark:border-gray-700 {getBtnTextClass(true)}" disabled={true}>
                        ...
                    </button>
                {:else}
                    {@const disabled = i === $pageNum}
                    <li>
                        <button onclick={() => setToPageNum(i)} class="flex items-center justify-center px-4 h-10 leading-tight bg-white border border-gray-300 dark:bg-gray-800 dark:border-gray-700 {getBtnTextClass(disabled)} {getHoverBtnClass(disabled)}" {disabled}>
                            {i}
                        </button>
                    </li>
                {/if}
            {/each}
            <li>
                <button type="button" onclick={onNext} class="flex items-center justify-center px-4 h-10 leading-tight bg-white border border-gray-300 rounded-e-lg dark:bg-gray-800 dark:border-gray-700 {getHoverBtnClass(nextBtnDisabled)} {getBtnTextClass(nextBtnDisabled)}" disabled={nextBtnDisabled}>
                    <Translate spanClass="sr-only" text="Next" />
                    <svg class="w-3 h-3 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 6 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 9 4-4-4-4"/>
                    </svg>
                </button>
            </li>
        </ul>
    </nav>
{/if}
