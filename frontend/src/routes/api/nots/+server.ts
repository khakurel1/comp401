import { type RequestHandler } from '@sveltejs/kit';
import { BASE_API_URI } from "$lib/utils/constants";

export const GET: RequestHandler = async ({ locals: { auth }, cookies, params }) => {
    if (!auth) {
        return new Response(JSON.stringify({
            message: "not authorized",
        }))
    }

    const token = cookies.get('jwt');
    const res = await fetch(
        `http://${BASE_API_URI}/notifications/`,
        {
            method: "GET",
            headers: {
                Authorization: "Bearer " + token,
                "Content-Type": "application/json",
            },
        },
    );
    if (!res.ok) {
        return new Response(JSON.stringify(
            await res.json()
        ))
    }
    const data = await res.json()
    return new Response(JSON.stringify(data));
};
