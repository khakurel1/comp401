<script lang="ts">
    import StatSection from "$components/StatSection.svelte";
    import Table from "$components/table/Table.svelte";
    import Topbar from "$components/Topbar.svelte";
    import type { PageData } from "./$types";
    import type { Evaluation, Ticker } from "../../types";
    import { enhance } from "$app/forms";
    import type { SubmitFunction } from "@sveltejs/kit";
    import type { ActionData } from "./$types";

    export let data: PageData;
    export let form: ActionData;

    let query = "";
    let evaluations = data.evaluations;
    let hideSuggestion = true;
    let showModal = false;

    let displayed_evals = evaluations;
    let filtered: Ticker[] = [];
    let selected: Ticker[] = [];

    const submitCreate: SubmitFunction = () => {
        return async ({ result, update }) => {
            if (result.type == "success" && result.data?.evaluation) {
                // evaluations.push(result.data?.evaluation as Evaluation);
                evaluations = [result.data?.evaluation as Evaluation].concat(evaluations)
                evaluations = [...evaluations];
                displayed_evals = [...evaluations];
            }
            update();
        };
    };

    let timeoutId: number;
    function handleInput(e: InputEvent) {
        if (String(e.target?.value).length < 2) {
            return;
        }
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(async () => {
            let query = e.target?.value;
            const response = await fetch(`/api/tickers/?name=${query}`, {
                headers: {
                    "content-type": "application/json",
                },
            });

            const data = await response.json();
            filtered = data.tickers;
        }, 600);
    }
</script>

<dialog id="my_modal_2" class="modal">
    <div class="modal-box min-h-fit">
        <form
            method="POST"
            action="?/create"
            use:enhance={submitCreate}
            class="flex justify-between"
        >
            <h3 class="font-bold text-lg">Add Evaluation</h3>
            <input
                name="selected"
                type="hidden"
                value={JSON.stringify(selected)}
            />
            <button
                class="btn btn-sm max-w-xl bg-white border-1 border-emerald-500 text-emerald-500 hover:text-white hover:bg-emerald-500"
                type="submit"
            >
                Done
            </button>
        </form>

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
        {#if form?.missing}
            <span class="text-red-400"> Select 4 tickers to continue </span>
        {:else if form?.error}
            <span class="text-red-400"> Some error occured! </span>
        {/if}
        <div class="py-4 relative">
            <input
                class="input input-bordered focus:border-brown w-full !outline-0 text-slate-700"
                on:focus={() => (hideSuggestion = false)}
                on:input={handleInput}
            />
            {#if filtered.length > 0}
                <ul
                    class="border border-slate-300 rounded-xl py-1 w-full my-1 max-h-60 overflow-y-scroll overflow-hidden"
                    class:hidden={hideSuggestion}
                >
                    {#each filtered as s}
                        <button
                            class="hover:bg-slate-100 py-2 px-4 w-full text-left"
                            on:click={() => {
                                if (selected.length > 3) return;

                                for (let sec of selected) {
                                    if (sec.name == s.name) {
                                        return;
                                    }
                                }

                                selected.push(s);
                                selected = [...selected];
                            }}
                        >
                            <span class="font-semibold text-sm">
                                {s.symbol}
                            </span>
                            <span class="font-light text-slate-400 text-xs">
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

<nav class="absolute top-12 left-0 w-full z-10 p-4">
    <div
        class="w-full items-center flex justify-between md:flex-nowrap flex-wrap md:px-10 px-4"
    >
        <!-- <a -->
        <!--     class="text-lg uppercase hidden lg:inline-block font-semibold" -->
        <!--     href="#pablo">Dashboard</a -->
        <!-- > -->
        <form class="md:flex hidden flex-row flex-wrap items-center lg:ml-auto">
            <input
                bind:value={query}
                on:input={async (l) => {
                    displayed_evals= evaluations.filter((e) => {
                        const hasName =
                            e.attributes.tickers.findIndex((i) => {
                                return i.name
                                    .toString()
                                    .toLowerCase()
                                    .includes(
                                        l.currentTarget.value.toLowerCase(),
                                    );
                            }) != -1;
                        const hasSymbol =
                            e.attributes.tickers.findIndex((i) => {
                                return i.symbol
                                    .toString()
                                    .toLowerCase()
                                    .includes(
                                        l.currentTarget.value.toLowerCase(),
                                    );
                            }) != -1;
                        return hasName || hasSymbol;
                    });
                    displayed_evals = [...displayed_evals];
                    // update()
                }}
                type="text"
                placeholder="Type here"
                class="input input-bordered border-brown w-full max-w-xs !outline-0 text-slate-700"
                required
            />
        </form>
    </div>
</nav>

<StatSection />
<Table evaluations={displayed_evals} />

<button
    onclick="my_modal_2.showModal()"
    class="btn btn-sm max-w-xl bg-white border-1 border-emerald-500 text-emerald-500 hover:text-white hover:bg-emerald-500 mx-3 md:mx-14 mb-10"
    type="submit"
>
    + Add new evaluation
</button>
