import { redirect, type Actions, fail, type RequestEvent, } from "@sveltejs/kit";
import type { Evaluation, Ticker } from "../../types";
import { BASE_API_URI } from "$lib/utils/constants"
import type { PageServerLoadEvent } from "../$types";

export async function load({ locals: { auth }, cookies }: PageServerLoadEvent) {
    if (!auth) {
        throw redirect(301, "/auth/login")
    }

    const jwt = cookies.get('jwt');
    const res = await fetch(`http://${BASE_API_URI}/evaluations?limit=20`, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + jwt,
            'Content-Type': 'application/json'
        }),
    });
    if (res.status == 403) {
        throw redirect(301, "/auth/login")
    }
    const data = await res.json()
    return {
        evaluations: data.data as Evaluation[]
    }
};


export const actions = {
    create: async ({ locals: { auth }, request, cookies }: RequestEvent) => {
        if (!auth) throw redirect(301, "/auth/login")
        const jwt = cookies.get('jwt');
        const data = await request.formData()
        const tickers = data.get("selected")
        if (!tickers) {
            return fail(400, { missing: true })
        }
        const parsed = JSON.parse(tickers.toString()) as Ticker[]

        if (parsed.length != 4) {
            return fail(400, { missing: true })
        }

        const res = await fetch(`http://${BASE_API_URI}/evaluations`, {
            method: "POST",
            headers: {
                Authorization: "Bearer " + jwt,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tickers: JSON.stringify(parsed),
            }),
        });
        if (res.status == 403) {
            throw redirect(301, "/auth/login");
        } else if (!res.ok) {
            return fail(400, { error: true })
        }

        const response = await res.json();
        return { success: true, evaluation: response.data as Evaluation }
    },
} satisfies Actions;

