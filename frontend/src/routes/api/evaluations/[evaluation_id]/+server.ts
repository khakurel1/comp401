import { type RequestHandler } from '@sveltejs/kit';
import { BASE_API_URI } from "$lib/utils/constants";

export const POST: RequestHandler = async ({ locals: { auth }, cookies, params }) => {
    if (!auth) {

        return new Response(JSON.stringify({
            message: "not authorized",
        }))
    }

    const token = cookies.get('jwt');
    const res = await fetch(
        `http://${BASE_API_URI}/evaluations/?evaluation_id=${params.evaluation_id}`,
        {
            method: "DELETE",
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
    return new Response(JSON.stringify({
        success: `evaluation with id: ${params.evaluation_id} deleted successfully.`
    }));
};
