<script lang="ts">
    import type { Evaluation } from "../../types";
    import TableEntry from "./TableEntry.svelte";

    export let evaluations: Evaluation[] = [];
</script>

<div class="px-8 md:px-10 mx-2 md:mx-4">
    <div
        class="relative flex flex-col w-full mb-6 shadow-lg rounded-lg bg-white border border-brown w-full bg-white z-20 pb-4"
    >
        <h3 class="py-4 px-8 font-semibold text-lg text-blueGray-700 flex justify-between">
            My Evaluations
        <!-- <button -->
        <!--     class="btn btn-sm max-w-ws bg-white border-1 border-emerald-400 text-emerald-400 hover:text-white hover:bg-emerald-400" -->
        <!--     type="submit" -->
        <!-- > -->
        <!--     + add new evaluation -->
        <!-- </button> -->
        </h3>
        <div class="w-full overflow-x-auto px-2">
            <table class="items-center w-full bg-transparent border-collapse">
                <thead
                    class="text-xs uppercase font-semibold text-left border border-solid border-x-0"
                >
                    <tr>
                        <th class="px-6 align-middle py-3">Id</th>
                        <th class="px-6 align-middle py-3">Ticker #1</th>
                        <th class="px-6 align-middle py-3">Ticker #2</th>
                        <th class="px-6 align-middle py-3">Ticker #3</th>
                        <th class="px-6 align-middle py-3">Ticker #4</th>
                        <th class="px-6 align-middle py-3">Date</th>
                        <th class="px-6 align-middle py-3" />
                    </tr>
                </thead>
                <tbody>
                    {#each evaluations as evaluation}
                        <TableEntry {evaluation} />
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>
