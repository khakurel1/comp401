<!-- TODO:3. Before the completion of task show a loading screen/ or not sufficient data in evaluations[id] page -->
<!-- TODO:4. Prettify the Pie Chart with larger Labels and show percentage -->
<!-- TODO:5. Prettify graph -->
<!-- TODO:6. Show current ticker adj close value -->
<!-- TODO:7. Format additional data in table -->
<script lang="ts">
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { JSXGraph } from "jsxgraph";
    import type { PageData } from "./$types";
    import { calculate_percent_Mark } from "$lib/utils/helpers";
    import type { Ticker } from "../../../../types";

    export let data: PageData;
    const evaluation = data.evaluation;
    let frontier: Map<string, { wts: number[]; sd: number }>;

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

    let closed_vals = {};

    let chartData: number[] = [];
    if (evaluation.attributes.data) {
        evaluation.attributes.data = JSON.parse(
            evaluation.attributes.data as string, // can ignore because this is a json in itself
        );
        frontier = evaluation.attributes.data.efficient_frontier;

        // closed_vals =

        let board;
        onMount(() => {
            board = JSXGraph.initBoard("jxgbox", {
                boundingbox: [-10, 50, 80, -10], // first x-axis, second y-axis
                axis: true,
                defaultAxes: {
                    x: {
                        name: "Standard Deviation(%)",
                        withLabel: true,
                        label: {
                            rotate: 0,
                            fontSize: 18,
                            offset: [-20, -50],
                            position: "bot",
                        },
                    },
                    y: {
                        withLabel: true,
                        name: "Expected Return(%)",
                        label: {
                            rotate: 90,
                            fontSize: 18,
                            offset: [-50, 10],
                            position: "bot",
                        },
                    },
                },
            });

            // var y = [0.151, 0.154, 0.171, 0.202, 0.243, 0.289, 0.341, 0.397, 0.455];
            // var x = [7, 8, 9, 10, 11, 12, 13, 14, 15];
            // var y = [12.97, 13.37, 14.37, 15.37, 16.37, 17.37, 18.37, 19.37, 20.37];
            // var x = [15.1, 15.4, 17.1, 20.0, 24.3, 28.9, 34.1, 39.7, 45.5];
            let x = [];
            let y = [];

            let entries = Object.keys(frontier).sort((a, b) => a - b);

            for (var i = 0; i < entries.length; i++) {
                let key = entries[i];
                let ret =
                    (Number(key) < 1 ? Number(key) * 100 : Number(key)) +
                    evaluation.attributes.data.gs1 * 100;
                let sd = Number(frontier[key]["sd"]) * 100;

                console.log(Number(key), ret, evaluation.attributes.data.gs1);
                y.push(ret);
                x.push(sd);
            }

            var graph = board.create("spline", [x, y], {
                strokeWidth: 2, // Optional: Set the width of the line
            });

            // Draw the tangent line
            // let g1 = board.create("glider", [graph]);
            // var tangent = board.create("tangent", [g1]);

            var line = board.create(
                "line",
                [
                    [0, evaluation.attributes.data.gs1 * 100],
                    [
                        evaluation.attributes.data.max_sharpie_ratio_sd * 100,
                        evaluation.attributes.data
                            .max_sharpie_ratio_expected_return * 100,
                    ],
                ],
                {
                    strokeColor: "#00ff00", // Optional: Set the color of the line
                    strokeWidth: 2, // Optional: Set the width of the line
                },
            );
            let point_3_1 = calculate_percent_Mark(
                0,
                evaluation.attributes.data.gs1 * 100,
                evaluation.attributes.data.max_sharpie_ratio_sd * 100,
                evaluation.attributes.data.max_sharpie_ratio_expected_return *
                    100,
                evaluation.attributes.data.y,
            );
            var point_div = board.create("point", [point_3_1.x, point_3_1.y], {
                name: "Complete Portfolio", // Optional: Set the name of the point
                size: 2, // Optional: Set the size of the point
                face: "o", // Optional: Set the face of the point
            });
            var point = board.create(
                "point",
                [
                    evaluation.attributes.data.max_sharpie_ratio_sd * 100,
                    evaluation.attributes.data
                        .max_sharpie_ratio_expected_return * 100,
                ],
                {
                    name: "Optimal Risky Portfolio", // Optional: Set the name of the point
                    size: 2, // Optional: Set the size of the point
                    face: "o", // Optional: Set the face of the point
                },
            );

            chartData = [];
            let total = 0;
            console.log("calc");
            evaluation.attributes.data.optimal_weights.forEach((i) => {
                total = total + i;
                chartData.push(i * evaluation.attributes.data.y);
                console.log(
                    i,
                    evaluation.attributes.data.y,
                    i * evaluation.attributes.data.y,
                );
            });
            chartData.push((1 - total) * evaluation.attributes.data.y);

            chartData.push(1 - evaluation.attributes.data.y);

            var board = JXG.JSXGraph.initBoard("piechart", {
                showNavigation: false,
                showCopyright: true,
                boundingbox: [-8, 8, 8, -8],
            });
            // board.containerObj.style.backgroundColor = "black";
            board.options.label.strokeColor = "green";
            board.options.label.fontSize = 16;

            let labels = evaluation.attributes.tickers.map(
                (t, idx) =>
                    `${t.symbol} - ${(chartData[idx] * 100).toFixed(3)}%`,
            );
            labels.push(`Risk Free - ${(chartData[chartData.length-1]*100).toFixed(3)}%`);
            var pieChart = board.create("chart", chartData, {
                chartStyle: "pie",
                colors: ["#0F408D", "#6F1B75", "#CA147A", "#DA2228", "#E8801B"],
                fillOpacity: 0.8,
                center: [0, 0],
                strokeColor: "black",
                highlightStrokeColor: "black",
                strokeWidth: 2,
                labels: labels,
                highlightColors: [
                    "#E46F6A",
                    "#F9DF82",
                    "#F7FA7B",
                    "#B0D990",
                    "#69BF8E",
                ],
                highlightOnSector: true,
                highlightBySize: true,
            });
        });
    }

    function sumArray(arr: number[]) {
        let sum = 0;
        for (let i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
</script>

{#if evaluation.attributes.data}
    <section class="py-16 mx-1 md:mx-8 min-h-screen pt-[18rem] px-2">
        <div
            class="relative flex flex-col min-w-0 break-words bg-white mb-6 rounded-lg -mt-64 border border-slate-700 pb-10"
        >
            <div class="md:px-12">
                <div class="text-center mt-8 space-y-20">
                    <div class="text-sm font-semibold mb-2 text-right">
                        Created at: {evaluation.attributes.created_at}
                    </div>

                    <div>
                        <div
                            class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left"
                        >
                            Tickers:
                        </div>

                        <div>
                            <table
                                class="items-center bg-transparent border-collapse w-full"
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
                                            >At: {evaluation.attributes
                                                .created_at}</th
                                        >
                                        <!-- <th -->
                                        <!--     class="px-6 text-center align-middle py-3" -->
                                        <!--     >Today: {datetime}</th -->
                                        <!-- > -->
                                    </tr>
                                </thead>
                                <tbody>
                                    {#each evaluation.attributes.tickers as ticker}
                                        <tr class="">
                                            <td class="text-left">
                                                {ticker.name}
                                            </td>
                                            <td> {ticker.symbol} </td>
                                            <td>
                                                {evaluation.attributes.data.closed_values[
                                                    ticker.symbol
                                                ].toFixed(3)}
                                            </td>
                                            <!-- <td> -->
                                            <!--     {evaluation.attributes.data.closed_values[ -->
                                            <!--         ticker.symbol -->
                                            <!--     ].toFixed(3)} -->
                                            <!--     {#if Math.random() < 0.5} -->
                                            <!--         <span -->
                                            <!--             class="text-emerald-400" -->
                                            <!--             >+ {Math.random().toPrecision( -->
                                            <!--                 2, -->
                                            <!--             )}%</span -->
                                            <!--         > -->
                                            <!--     {:else} -->
                                            <!--         <span class="text-red-400" -->
                                            <!--             >- {Math.random().toPrecision( -->
                                            <!--                 2, -->
                                            <!--             )}%</span -->
                                            <!--         > -->
                                            <!--     {/if} -->
                                            <!-- </td> -->
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {#if evaluation.attributes.data == null}
                        <div>Loading...</div>
                    {:else}
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
                                                >Optimal Weights</th
                                            >
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each evaluation.attributes.tickers as ticker, idx}
                                            <tr class="">
                                                <td> {ticker.symbol} </td>

                                                <td>
                                                    {#if evaluation.attributes.tickers.length - 1 == idx}
                                                        {(
                                                            (1 -
                                                                sumArray(
                                                                    evaluation
                                                                        .attributes
                                                                        .data
                                                                        .optimal_weights,
                                                                )) *
                                                            100
                                                        ).toFixed(3)}
                                                    {:else}
                                                        {(
                                                            evaluation
                                                                .attributes.data
                                                                .optimal_weights[
                                                                idx
                                                            ] * 100
                                                        ).toFixed(3)}
                                                    {/if}%
                                                </td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- <div -->
                        <!--     class="mt-10 py-10 border-t border-blueGray-200 text-center" -->
                        <!-- > -->
                        <!--     <h4 -->
                        <!--         class="text-lg leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left" -->
                        <!--     > -->
                        <!--         Steps: -->
                        <!--     </h4> -->
                        <!-- </div> -->

                        <div>
                            <div
                                class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left"
                            >
                                Variance-Covariance Matrix:
                            </div>
                            <table
                                class="w-full items-center w-full bg-transparent border-collapse"
                            >
                                <thead
                                    class="uppercase font-semibold border border-solid border-x-0"
                                >
                                    <tr>
                                        <th />
                                        {#each evaluation.attributes.tickers as ticker}
                                            <th class="py-3">
                                                {ticker.symbol}
                                            </th>
                                        {/each}
                                    </tr>
                                </thead>

                                <tbody>
                                    {#each evaluation.attributes.data.varcovar as var_covar, idx}
                                        <tr>
                                            <td class="font-bold">
                                                {evaluation.attributes.tickers[
                                                    idx
                                                ].symbol}
                                            </td>
                                            {#each var_covar as co}
                                                <td>
                                                    {co}
                                                </td>
                                            {/each}
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>

                        <div>
                            <div
                                class="text-sm leading-normal mt-0 mb-2 text-blueGray-400 font-bold uppercase text-left"
                            >
                                Efficient Fontier:
                            </div>
                            <table
                                class="w-full items-center w-full bg-transparent border-collapse"
                            >
                                <thead
                                    class="uppercase font-semibold border border-solid border-x-0"
                                >
                                    <tr>
                                        <th class="py-3 w-1/2"> X </th>
                                        <th class="py-3 w-1/2"> Y </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {#each Object.keys(evaluation.attributes.data.efficient_frontier) as key}
                                        <tr>
                                            <td class="">
                                                {key}%
                                            </td>
                                            <td class="">
                                                {(
                                                    evaluation.attributes.data
                                                        .efficient_frontier[key]
                                                        .sd * 100
                                                ).toFixed(3)}%
                                            </td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                        <!-- {JSON.stringify(evaluation.attributes.data)} -->
                        <!-- {JSON.stringify(chartData)} -->
                        <span class="font-bold">
                            Expected rate of return: {(
                                evaluation.attributes.data.expected_return * 100
                            ).toFixed(3)}
                        </span>
                        |
                        <span class="font-bold">
                            Standard Deviation: {(
                                evaluation.attributes.data
                                    .max_sharpie_ratio_sd * 100
                            ).toFixed(3)}
                        </span>
                        <div
                            id="jxgbox"
                            class="w-3/5 mx-auto"
                            style="aspect-ratio: 1/1;"
                        ></div>

                        <span class="text-lg w-full text-center my-6"
                            >Fig: Complete Portfolio ({(
                                evaluation.attributes.data.y * 100
                            ).toFixed(3)}% risky portfolio, {(
                                (1 - evaluation.attributes.data.y) *
                                100
                            ).toFixed(3)}% risk-free asset)</span
                        >

                        <div
                            id="piechart"
                            class="w-3/5 mx-auto my-0"
                            style="aspect-ratio: 1/1;"
                        ></div>

                        <span class="text-lg w-full text-center my-1"
                            >Fig: Pie Chart</span
                        >
                    {/if}
                    <button
                        class="btn max-w-ws mt-4 bg-white border-1 border-red-400 text-red-400 hover:text-white hover:bg-red-400 w-full"
                        on:click={async () => {
                            const resp = await fetch(
                                `/api/evaluations/${evaluation.id}/`,
                                {
                                    method: "POST",
                                },
                            );
                            if (resp.ok) {
                                goto("/dashboard");
                            }
                        }}
                    >
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </section>
{:else}
    <center class="h-screen items-center flex justify-center">
        <div>
            <h1 class="text-3xl font-bold text-slate-600">
                Some Error Occured!!
            </h1>

            <button
                class="btn max-w-ws mt-4 bg-white border-1 border-red-400 text-red-400 hover:text-white hover:bg-red-400 w-full"
                on:click={async () => {
                    const resp = await fetch(
                        `/api/evaluations/${evaluation.id}/`,
                        {
                            method: "POST",
                        },
                    );
                    if (resp.ok) {
                        goto("/dashboard");
                    }
                }}
            >
                Delete Evaluation
            </button>
        </div>
    </center>
{/if}
