import { type RequestHandler } from '@sveltejs/kit';
import { BASE_API_URI } from "$lib/utils/constants"

export const GET: RequestHandler = async ({ url, locals: { auth }, cookies, fetch }) => {
    if (!auth) {
        return new Response(JSON.stringify({
            message: "not authorized",
        }))
    }

    const token = cookies.get('jwt');

    // const read = url.searchParams.get("read") || "true"
    const res = await fetch(`http://${BASE_API_URI}/notifications?read=true&limit=200`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
        },
    });
    if (!res.ok) {
        const response = await res.json()
        return new Response(JSON.stringify(response))
    }

    const data = await res.json()
    return new Response(JSON.stringify(data));
};
