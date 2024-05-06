<script lang="ts">
    import { enhance } from "$app/forms";
    import { goto } from "$app/navigation";
    import type { Writable } from "svelte/store";
    import type { ActionData, SubmitFunction } from "./$types";
    import { getContext } from "svelte";

    export let form: ActionData;
    let user = getContext<Writable<string>>("user");

    const submitSignup: SubmitFunction = () => {
        return async ({ result, update }) => {
            if (result.type == "success" && result.data?.jwt) {
                user.set(result.data.jwt);
                return goto("/dashboard");
            }
            update();
        };
    };
</script>

<h1 class="text-2xl font-bold">Sign up</h1>

<form method="POST" use:enhance={submitSignup}>
    <div class="form-control w-full max-w-xs text-left space-y-3">
        <label class="label" for="username">
            <span class="label-text font-semibold text-brown"> Username </span>
        </label>
        <input
            name="username"
            class="input input-bordered focus:border-brown w-full max-w-xs !outline-0 text-slate-700"
        />

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

        <label class="label" for="confirm">
            <span class="label-text font-semibold text-brown">
                Confirm Password
            </span>
        </label>
        <input
            name="confirm"
            type="password"
            class="input input-bordered focus:border-brown w-full max-w-xs !outline-0 text-slate-700"
        />

        <button
            class="btn max-w-ws mt-4 bg-white border-1 border-slate-400 text-brown hover:text-white hover:bg-slate-300"
            type="submit"
        >
            Signup
        </button>

        {#if form?.missing}
            <div class="block notification is-danger text-red-600">
                field missing
            </div>
        {:else if form?.mismatch}
            <div class="block notification is-danger text-red-600">
                password fields not matching
            </div>
        {:else if form?.incorrect}
            <div class="block notification is-danger text-red-600">
                fields incorrect
            </div>
        {/if}
    </div>
</form>
