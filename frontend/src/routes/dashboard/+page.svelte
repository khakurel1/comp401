<script lang="ts">
    import StatSection from "$components/StatSection.svelte";
    import Table from "$components/table/Table.svelte";
    import Topbar from "$components/Topbar.svelte";
    import type { PageData } from "./$types";
    import type { Evaluation, Ticker } from "../../types";
    import { authStore } from "$store/auth";
    import { goto } from "$app/navigation";

    export let data: PageData;

    let hideSuggestion = true;
    let hideError = true;
    let suggestions: Ticker[] = [
        { name: "ticker 1", symbol: "TIC1" },
        { name: "ticker 2", symbol: "TIC2" },
        { name: "ticker 3", symbol: "TIC3" },
        { name: "ticker 4", symbol: "TIC4" },
    ];

    let filtered: Ticker[] = [];

    let selected: Ticker[] = [];

    async function addNewEvaluation() {
        if (selected.length < 4) {
            hideError = false;
            return;
        } else {
            hideError = true;
        }

        const jwt = localStorage.getItem("jwt")?.toString();

        const resp = await fetch("http://localhost:8081/evaluations", {
            method: "POST",
            headers: {
                Authorization: "Bearer " + jwt,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tickers: JSON.stringify(selected),
            }),
        });
        if (resp.status == 403) {
            goto("/auth/login");
        }

        const respJson = await resp.json();
        data.evaluations.push(respJson.eval as Evaluation);
        data.evaluations = [...data.evaluations];
    }
</script>

<dialog id="my_modal_2" class="modal">
    <div class="modal-box min-h-fit">
        <div class="flex justify-between">
            <h3 class="font-bold text-lg">Add Evaluation</h3>
            <button
                class="btn btn-sm max-w-xl bg-white border-1 border-emerald-500 text-emerald-500 hover:text-white hover:bg-emerald-500"
                on:click={async () => await addNewEvaluation()}
            >
                Done
            </button>
        </div>

        <div class="w-full space-x-1">
            {#each selected as entry}
                <button
                    id={entry.symbol}
                    class="border rounded border-slate-400 px-2 hover:border-red-400 hover:text-red-400"
                    on:click={(e) => {
                        let item = e.currentTarget.id;
                        const index = selected.findIndex(
                            (i) => i.symbol == item,
                        );
                        if (index > -1) {
                            selected.splice(index, 1);
                        }
                        selected = [...selected];
                    }}
                >
                    {entry.symbol} <span class="ml-2">x</span>
                </button>
            {/each}
        </div>
        <span class="text-red-400" class:hidden={hideError}>
            Select 4 tickers to continue
        </span>
        <div class="py-4 relative">
            <input
                class="input input-bordered focus:border-brown w-full !outline-0 text-slate-700"
                on:focus={() => (hideSuggestion = false)}
                on:input={(e) => {
                    let data = e.currentTarget.value;
                    filtered = suggestions.filter(
                        (i) => i.symbol.includes(data) || i.name.includes(data),
                    );
                    console.log(filtered);
                    filtered = [...filtered];
                }}
            />
            {#if filtered.length > 0}
                <ul
                    class="border border-slate-300 rounded-xl py-1 w-full"
                    class:hidden={hideSuggestion}
                >
                    {#each filtered as s}
                        <button
                            class="hover:bg-slate-100 py-2 px-4 w-full text-left"
                            on:click={() => {
                                if (selected.length > 3) return;
                                selected.push(s);
                                selected = [...selected];
                            }}
                        >
                            <span class="font-semibold">
                                {s.symbol}
                            </span>
                            <span class="font-light text-slate-400">
                                {s.name}
                            </span>
                        </button>
                    {/each}
                </ul>
            {/if}
        </div>
    </div>
    <form method="dialog" class="modal-backdrop">
        <button>close</button>
    </form>
</dialog>

<Topbar />
<StatSection />
<Table evaluations={data.evaluations} />

<button
    onclick="my_modal_2.showModal()"
    class="btn btn-sm max-w-xl bg-white border-1 border-emerald-500 text-emerald-500 hover:text-white hover:bg-emerald-500 mx-14 mb-10"
    type="submit"
>
    + Add new evaluation
</button>
