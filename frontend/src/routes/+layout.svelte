<script>
    import { onMount, setContext } from "svelte";
    import "../app.css";
    import { authStore } from "$store/auth";

    // onMount(()=>{
    //     const jwt = window.localStorage.getItem("jwt")
    //     if (!jwt) return
    //
    // })
    //
</script>

<div class="app text-brown">
    <main>
        <slot />
    </main>
</div>
