import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "../../../$types";
import { HOST } from "../../../../config";

export const load: PageServerLoad = async ({ params, cookies }) => {
    const jwt = cookies.get('jwt');
    if (!jwt)
        redirect(301, "/auth/login")

    const res = await fetch(`http://${HOST}/evaluations/${params.evaluation_id}`, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + jwt,
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
