import { type RequestHandler } from '@sveltejs/kit';
import { BASE_API_URI } from "$lib/utils/constants";

export const POST: RequestHandler = async ({ url, locals: { auth }, cookies, params }) => {
    if (!auth) {
        return new Response(JSON.stringify({
            message: "not authorized",
        }))
    }

    const jwt = cookies.get('jwt');
    const res = await fetch(`http://${BASE_API_URI}/notifications/${params.notification_id}/read`, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + jwt,
        }),
    });
    if (!res.ok) {
        return new Response(JSON.stringify({
            message: "error",
        }))
    }
    return new Response(JSON.stringify({
        success: "notifications read successfully."
    }));
};
