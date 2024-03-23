<script lang="ts">
    import { goto } from "$app/navigation";
    import type { Evaluation } from "../../../../types";
    import type { PageData } from "./$types";
    import { HOST } from "../../../../config";

    export let data: PageData;
    const evaluation = data.evaluation as Evaluation;

    var currentdate = new Date();
    var datetime =
        currentdate.getDate() +
        "/" +
        (currentdate.getMonth() + 1) +
        "/" +
        currentdate.getFullYear() +
        " @ " +
        currentdate.getHours() +
        ":" +
        currentdate.getMinutes() +
        ":" +
        currentdate.getSeconds();
</script>

<section class="py-16 mx-1 md:mx-8 min-h-screen pt-[18rem] px-2 ">
    <div
        class="relative flex flex-col min-w-0 break-words bg-white mb-6 shadow-lg rounded-lg -mt-64 border border-slate-700"
    >
        <div class="md:px-12">
            <div class="text-center mt-8 space-y-20">
                <div class="text-sm font-semibold mb-2 text-right">
                    Created at: {evaluation.createdAt}
                </div>

                <div>
                    <div
                        class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left"
                    >
                        Tickers:
                    </div>

                    <div>
                        <table
                            class="items-center bg-transparent border-collapse"
                        >
                            <thead
                                class="text-sm uppercase font-semibold text-left border border-solid border-x-0"
                            >
                                <tr>
                                    <th
                                        class="px-6 text-center align-middle py-3"
                                        >Name</th
                                    >
                                    <th
                                        class="px-6 text-center align-middle py-3"
                                        >Symbols</th
                                    >
                                    <th
                                        class="px-6 text-center align-middle py-3"
                                        >At: {evaluation.createdAt}</th
                                    >
                                    <th
                                        class="px-6 text-center align-middle py-3"
                                        >Today: {datetime}</th
                                    >
                                </tr>
                            </thead>
                            <tbody>
                                {#each evaluation.tickers as ticker}
                                    <tr class="">
                                        <td class="text-left"> {ticker.name} </td>
                                        <td> {ticker.symbol} </td>
                                        <td> {ticker.symbol} </td>
                                        <td>
                                            {ticker.symbol}
                                            {#if Math.random() < 0.5}
                                                <span class="text-emerald-400"
                                                    >+ {Math.random().toPrecision(
                                                        2,
                                                    )}%</span
                                                >
                                            {:else}
                                                <span class="text-red-400"
                                                    >- {Math.random().toPrecision(
                                                        2,
                                                    )}%</span
                                                >
                                            {/if}
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div>
                    <div
                        class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left"
                    >
                        Weights:
                    </div>

                    <div>
                        <table
                            class="items-center w-full bg-transparent border-collapse"
                        >
                            <thead
                                class="text-xs uppercase font-semibold text-left border border-solid border-x-0"
                            >
                                <tr>
                                    <th
                                        class="px-6 text-center align-middle py-3"
                                        >Symbols</th
                                    >
                                    <th
                                        class="px-6 text-center align-middle py-3"
                                        >Weights</th
                                    >
                                </tr>
                            </thead>
                            <tbody>
                                {#each evaluation.tickers as ticker}
                                    <tr class="">
                                        <td> {ticker.symbol} </td>
                                        <td>
                                            {(Math.random() * 100).toPrecision(
                                                4,
                                            )}%
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="mt-10 py-10 border-t border-blueGray-200 text-center">
                <h4
                    class="text-lg leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left"
                >
                    Steps:
                </h4>
            </div>
        </div>

        <button
            class="btn max-w-ws mt-4 bg-white border-1 border-red-400 text-red-400 hover:text-white hover:bg-red-400 m-8"
            on:click={async () => {
                const jwt = localStorage.getItem("jwt")?.toString();

                const resp = await fetch(
                    `http://${HOST}/evaluations/?evaluation_id=${evaluation.id}`,
                    {
                        method: "DELETE",
                        headers: {
                            Authorization: "Bearer " + jwt,
                            "Content-Type": "application/json",
                        },
                    },
                );
                if (resp.status == 403) {
                    goto("/auth/login");
                }

                if (resp.status == 200) {
                    goto("/dashboard");
                }
            }}
        >
            Delete
        </button>
    </div>
</section>
