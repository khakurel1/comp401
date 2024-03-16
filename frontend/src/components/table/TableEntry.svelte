<script lang="ts">
    import type { Evaluation } from "../../types";

    export let evaluation: Evaluation;
</script>

<tr class="hover:bg-gray-100">
    <th
        class="border-t-0 px-6 align-middle border-l-0 border-r-0 text-xs whitespace-nowrap p-4 text-left flex items-center "
    >
        <a href="/dashboard/evaluations/{evaluation.id}" class="hover:underline">
            {evaluation.id.slice(0, 8)}
        </a>
    </th>

    {#each evaluation.tickers as ticker}
        <td class="px-6 text-xs p-4">{ticker.symbol}</td>
    {/each}

    <td class="px-2 text-xs p-4 font-bold">
        <button class="w-full text-left"> {evaluation.createdAt} </button>
    </td>
    <td class="px-2 text-xs p-4 font-bold">
        <button class="w-full"> : </button>
    </td>
</tr>
