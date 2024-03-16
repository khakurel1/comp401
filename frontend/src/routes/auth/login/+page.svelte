<script lang="ts">
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";
    import type { ActionData } from "./$types";

    export let form: ActionData;
</script>

<h1 class="text-2xl font-bold">Log in</h1>

<form
    method="POST"
    use:enhance={() => {
        return async ({ result, update }) => {
            if (result.type == "success" && result.data?.jwt) {

                window.localStorage.setItem(
                    "jwt",
                    result.data?.jwt?.toString(),
                );

                console.log("login successful!");
                return goto("/dashboard");
            }
            update();
        };
    }}
>
    <div class="form-control w-full max-w-xs text-left space-y-3">
        <label class="label" for="email">
            <span class="label-text font-semibold text-brown"> Email </span>
        </label>
        <input
            name="email"
            class="input input-bordered focus:border-brown w-full max-w-xs !outline-0 text-slate-700"
        />

        <label class="label" for="password">
            <span class="label-text font-semibold text-brown"> Password </span>
        </label>
        <input
            name="password"
            type="password"
            class="input input-bordered focus:border-brown w-full max-w-xs !outline-0 text-slate-700"
        />

        <button
            class="btn max-w-ws mt-4 bg-white border-1 border-slate-400 text-brown hover:text-white hover:bg-slate-300"
            type="submit"
        >
            Login
        </button>

        {#if form?.incorrect}
            <div class="block notification is-danger text-red-600 text-center">
                email and password didn't match.
            </div>
        {:else if form?.missing}
            <div class="block notification is-danger text-red-600 text-center">
                email or password missing.
            </div>
        {/if}
    </div>
</form>
