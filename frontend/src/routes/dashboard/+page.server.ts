import { redirect, type Actions, fail, } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import type { Evaluation, Ticker } from "../../types";
import { HOST } from "../../config"

export const load: PageServerLoad = async ({ cookies }) => {
    console.log("Apple", cookies.get("jwt"))
    const jwt = cookies.get('jwt');
    if (!jwt)
        redirect(301, "/auth/login")

    console.log(HOST)
    const res = await fetch(`http://${HOST}/evaluations?limit=20`, {
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
        evaluations: data.evaluations
    }
};


export const actions = {
    create: async ({ request, cookies }) => {
        const jwt = cookies.get('jwt');
        if (!jwt)
            redirect(301, "/auth/login")

        const data = await request.formData()
        const tickers = data.get("selected")
        if (!tickers) {
            return fail(400, { missing: true })
        }
        const parsed = JSON.parse(tickers.toString()) as Ticker[]

        if (parsed.length != 4) {
            return fail(400, { missing: true })
        }

        const resp = await fetch(`http://${HOST}/evaluations`, {
            method: "POST",
            headers: {
                Authorization: "Bearer " + jwt,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tickers: JSON.stringify(parsed),
            }),
        });
        if (resp.status == 403) {
            return redirect(301, "/auth/login");
        } else if (!resp.ok) {
            return fail(400, { error: true })
        }

        const respJson = await resp.json();
        return { success: true, evaluations: respJson as Evaluation }
    },
} satisfies Actions;
