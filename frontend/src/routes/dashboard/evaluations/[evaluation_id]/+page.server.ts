import { authStore } from "$store/auth";
import { redirect } from "@sveltejs/kit";

export const load = async ({ params }) => {
    if (authStore.value() == "")
        redirect(301, "/auth/login")

    const res = await fetch(`http://localhost:8081/evaluations/${params.evaluation_id}`, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + authStore.value(),
            'Content-Type': 'application/json'
        }),
    });
    if (res.status == 403) {
        redirect(301, "/auth/login")
    }
    const data = await res.json()
    return {
        evaluation: data.evaluation
    }
};
