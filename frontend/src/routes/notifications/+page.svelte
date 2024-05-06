<!-- DONE:8. Make Notification Pages look nicer -->
<script lang="ts">
    // TODO:2. Show any number of notifications
    import {type Notification} from "../../types";
    export let data;
    let notifications = (data.notifications || []) as Notification[];
</script>

<section class="py-16 mx-1 md:mx-8 min-h-screen py-[18rem] px-2">
    <div
        class="relative flex flex-col min-w-0 break-words bg-white mb-6 shadow-lg rounded-lg -mt-64 border border-slate-700 min-h-screen"
    >
        <div class="md:px-12">
            <div class="text-center mt-8 space-y-8">
                <div class="text-xl font-semibold mb-2 text-left">
                    Notifications
                </div>

                <div>
                    <ol class="space-y-1 mb-9 w-full">
                        {#each notifications as n, idx}
                            <li
                                class:text-slate-400={n.attributes.read}
                                class="transition ease-in-out delay-150 duration-300 text-left w-full"
                            >
                                <!-- {JSON.stringify(n)} -->
                                <button
                                    class="space-x-2 py-2 px-4 rounded border border-slate-800 bg-slate-50 hover:bg-slate-200 w-full flex"
                                    on:click={async (e) => {
                                        try {
                                            await fetch(
                                                `/api/notifications/${n.id}?read=true`,
                                                {
                                                    method: "POST",
                                                },
                                            );
                                            notifications[idx].attributes.read =
                                                true;
                                        } catch (e) {
                                            console.error(e);
                                        }
                                    }}
                                >
                                    <span
                                        class:text-emerald-500={n.attributes
                                            .success}
                                        class:text-red-500={!n.attributes
                                            .success}
                                    >
                                        {#if n.attributes.success}
                                            [Passed!]
                                        {:else}
                                            [Failed!]
                                        {/if}
                                    </span>
                                    <span>{n.id.slice(0, 6)}</span>
                                    <span>{n.attributes.created_at}</span>
                                    <span>
                                        Job completed for evaluation:
                                        <a
                                            on:click={(e) => {}}
                                            class="text-blue-400 underline hover:text-blue-500"
                                            href={`/dashboard/evaluations/${n.attributes.message}`}
                                            >{n.attributes.message}</a
                                        >
                                    </span>
                                </button>
                            </li>
                        {/each}
                    </ol>
                </div>
            </div>
        </div>
    </div>
</section>
