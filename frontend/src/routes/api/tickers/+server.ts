import type { RequestHandler } from './$types';
import { BASE_API_URI } from "$lib/utils/constants";

export const GET: RequestHandler = async ({ locals, url }) => {
    if (!locals.auth)
        return new Response(JSON.stringify({
            message: "not authorized",
        }))

    const name = String(url.searchParams.get('name') ?? "");
    const res = await fetch(`http://${BASE_API_URI}/tickers/?name=${name}&limit=10`, {
        method: 'GET',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
    });
    if (!res.ok) {
        const response = await res.json()
        return new Response(JSON.stringify(response))
    }
    const data = await res.json()
    return new Response(JSON.stringify(data));
};
