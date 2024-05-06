import { BASE_API_URI } from "$lib/utils/constants";
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    // console.log(event.locals.auth)
    if (event.locals.auth) {
        return await resolve(event);
    }

    const token = event.cookies.get('jwt');
    if (!token) {
        return await resolve(event);
    }

    const res = await fetch(`http://${BASE_API_URI}/auth/current_user/`, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }),
    })
    if (!res.ok) {
        return await resolve(event);
    }

    const response = await res.json();
    event.locals.auth = response.data;
    return await resolve(event);
}
