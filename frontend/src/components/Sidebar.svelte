<script>
    const routes = [
        {
            name: "History",
            href: "/dashboard",
        },
        // {
        //     name: "My Assets",
        //     href: "/dashboard/assets",
        // },
        {
            name: "Settings",
            href: "/dashboard/settings",
        },
        {
            name: "Logout",
            href: "/auth/logout",
        },
    ];
</script>

<nav
    class="md:left-0 md:absolute md:top-0 md:overflow-y-auto md:w-56 z-10 py-4 px-6 h-full border-r border-gray-100 max-w-sm"
>
    <div
        class="md:flex-col md:items-stretch md:min-h-full md:flex-nowrap px-0 flex flex-wrap items-center justify-between w-full mx-auto"
    >
        <div
            class="md:flex md:flex-col md:items-stretch md:opacity-100 md:relative md:mt-4 md:shadow-none shadow absolute top-0 left-0 right-0 z-40 overflow-y-auto overflow-x-hidden h-auto items-center flex-1 rounded hidden"
        >
            <h6
                class="md:min-w-full text-blueGray-500 text-sm uppercase font-bold block pt-1 pb-4 no-underline"
                data-svelte-h="svelte-1pbisl0"
            >
                Admin Dashboard
            </h6>
            <ul class="md:flex-col md:min-w-full flex flex-col list-none">
                {#each routes as route}
                    <li class="items-center hover:underline hover:bg-gray-50">
                        <a
                            href={route.href}
                            class="text-xs uppercase py-3 font-bold block text-blueGray-700 hover:text-blueGray-500"
                            ><i
                                class="fas fa-tv mr-2 text-sm text-blueGray-300"
                            />
                            {route.name}</a
                        >
                    </li>
                {/each}
            </ul>
        </div>
    </div>
</nav>
