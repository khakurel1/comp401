import { redirect } from "@sveltejs/kit";
import { BASE_API_URI } from "$lib/utils/constants";
import type { Evaluation } from "../../../../types";
import type { PageServerLoadEvent } from "../../../notifications/$types";

export const load = async ({ locals: { auth }, params, cookies }: PageServerLoadEvent) => {
    if (!auth)
        throw redirect(301, "/auth/login")

    const token = cookies.get('jwt');
    const res = await fetch(`http://${BASE_API_URI}/evaluations/${params.evaluation_id}`, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }),
    });
    if (res.status == 403) {
        throw redirect(301, "/auth/login")
    }
    const data = await res.json()
    return {
        evaluation: data.data as Evaluation
    }
};


export const ssr = false;
export const csr = true;
export const prerender = false;
export const trailingSlash = 'always';
