import { redirect } from "@sveltejs/kit";
import type { PageServerLoad, PageServerLoadEvent } from "./$types";
import { BASE_API_URI } from "$lib/utils/constants"
import type { Notification } from "../../types";

export const load = async ({ cookies, locals: { auth }, url }: PageServerLoadEvent) => {
    if (!auth) {
        throw redirect(301, "/auth/login")
    }

    const token = cookies.get('jwt');
    const res = await fetch(`http://${BASE_API_URI}/notifications?read=true&limit=200`, {
        method: 'GET',
        headers: new Headers({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
        }),
    });
    if (!res.ok) {
        return new Response(JSON.stringify({
            message: "error",
        }))
    }
    const response = await res.json()
    return { notifications: response.data } as { notifications: Notification[] }
};


// export const ssr = false;
// export const csr = true;
// export const prerender = false;
// export const trailingSlash = 'always';
