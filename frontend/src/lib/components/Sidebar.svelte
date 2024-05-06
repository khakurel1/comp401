<script lang="ts">
    import { onMount } from "svelte";
    import type { Notification } from "../../types";
    // TODO:1. Make notifications/error pop up when task completed
    const routes = [
        {
            name: "History",
            href: "/dashboard",
        },
        // {
        //     name: "My Assets",
        //     href: "/dashboard/assets",
        // },
        // {
        //     name: "Settings",
        //     href: "/dashboard/settings",
        // },
        {
            name: "Logout",
            href: "/auth/logout",
        },
    ];

    let past_not: number = 0;
    let notifications: number = 0;
    let count = 0;
    let showNotification = false;
    let notificationsCont = [] as Notification[];
    let currNotification: Notification;

    async function getNotifications() {
        try {
            const res = await fetch(`/api/nots`, {
                method: "GET",
                headers: new Headers({
                    "Content-Type": "application/json",
                }),
            });
            const response = await res.json();
            const data = response.data as Notification[];
            notificationsCont = data;
            console.log(notificationsCont.length);
            past_not = notifications;
            notifications = data.filter((n: Notification) => {
                if (!n.attributes.read) {
                    console.log(n);
                }
                return !n.attributes.read;
            }).length;

            if (notifications > past_not && count > 0) {
                // console.log("Notification changed", past_not);
                showNotification = true;
                currNotification =
                    notificationsCont[notificationsCont.length - 1];
                setTimeout(() => {
                    showNotification = false;
                }, 4000);
            }
            count += 1;
        } catch (e) {
            console.log("Error fetching notifications: ", e);
        }
    }

    onMount(async () => {
        await getNotifications();
        setInterval(async () => {
            await getNotifications();
        }, 3000);
    });

    function deleteAllCookies() {
        var cookies = document.cookie.split(";");

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];
            var eqPos = cookie.indexOf("=");
            var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie =
                name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }
    }
</script>

<nav
    class="md:left-0 md:absolute md:top-0 md:overflow-y-auto md:w-56 z-10 py-4 h-full border-r border-gray-100 max-w-sm"
>
    <div
        class="md:flex-col md:items-stretch md:min-h-full md:flex-nowrap px-0 flex flex-wrap justify-between w-full mx-auto"
    >
        <div
            class="md:flex md:flex-col md:items-stretch md:opacity-100 md:relative mt-12 md:shadow-none shadow absolute top-0 left-0 right-0 z-40 overflow-y-auto overflow-x-hidden h-auto items-center flex-1 rounded hidden"
        >
            <h3
                class="text-xl md:min-w-full text-blueGray-500 text-sm uppercase font-bold block pt-1 pb-4 no-underline px-6"
                data-svelte-h="svelte-1pbisl0"
            >
                Dashboard
            </h3>
            <div
                class="md:flex-col md:min-w-full flex flex-col list-none items-start text-sm"
            >
                {#each routes as route}
                    {#if route.name == "Logout"}
                        <button
                            class="hover:underline px-6 hover:bg-gray-50 w-full"
                            on:click={() => {
                                window.localStorage.removeItem("jwt");
                                deleteAllCookies();
                            }}
                        >
                            <a
                                href={route.href}
                                class="uppercase py-3 font-bold block text-blueGray-700 hover:text-blueGray-500"
                                ><i
                                    class="fas fa-tv mr-2 text-sm text-blueGray-300"
                                />
                                {route.name}</a
                            >
                        </button>
                    {:else}
                        <button
                            class="hover:underline px-6 hover:bg-gray-50 w-full"
                        >
                            <a
                                href={route.href}
                                class="uppercase py-3 font-bold block text-blueGray-700 hover:text-blueGray-500"
                                ><i
                                    class="fas fa-tv mr-2 text-sm text-blueGray-300"
                                />
                                {route.name}</a
                            >
                        </button>
                    {/if}
                {/each}
                <button
                    class="hover:underline px-6 hover:bg-gray-50 w-full text-left"
                >
                    <a
                        href="/notifications"
                        class="uppercase py-3 px-2 font-bold block text-blueGray-700 hover:text-blueGray-500"
                    >
                        Notifications
                        <div
                            class="badge badge-xs badge-secondary font-base bg-red-400"
                        >
                            {#if notifications}
                                {notifications}
                            {/if}
                        </div>
                    </a>
                </button>
            </div>
        </div>
    </div>
</nav>
{#if showNotification && notificationsCont.length > 0}
    <div class="toast toast-end z-[1000]">
        <div
            class="alert alert-success py-2 px-4 text-white bg-emerald-500"
            class:bg-red-400={!notificationsCont[notificationsCont.length - 1]
                ?.attributes.success}
        >
            <span
                >Completed Job for evaluation:
                <a
                    href={`/dashboard/evaluations/${currNotification.attributes.message}`}
                >
                    {currNotification.attributes.message}
                </a>
            </span>
        </div>
    </div>
{/if}
