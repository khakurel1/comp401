import { authStore } from "$store/auth";
import { redirect } from "@sveltejs/kit";

export const load = async ({ }) => {
    if (authStore.value() == "")
        redirect(301, "/auth/login")

    const res = await fetch("http://localhost:8081/evaluations", {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + authStore.value(),
            'Content-Type': 'application/json'
        }),
    });
    console.log(authStore.value());
    if (res.status == 403) {
        redirect(301, "/auth/login")
    }
    const data = await res.json()
    return {
        evaluations: data.evaluations
    }
};
