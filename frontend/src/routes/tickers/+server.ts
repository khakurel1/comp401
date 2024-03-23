import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { HOST } from '../../config';

export const GET: RequestHandler = async ({ url, cookies }) => {

    const jwt = cookies.get('jwt');
    if (!jwt)
        redirect(301, "/auth/login")
    const name = String(url.searchParams.get('name') ?? "");

    const res = await fetch(`http://${HOST}/tickers/?name=${name}&limit=10`, {
        method: 'GET',
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
    });
    if (!res.ok) {
        return new Response("error")
    }
    const data = await res.json()
    return new Response(JSON.stringify(data));
};
