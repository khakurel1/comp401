import { fail, type Actions, redirect } from '@sveltejs/kit';
import { BASE_API_URI } from '$lib/utils/constants';
import { formatError } from '$lib/utils/helpers';
import type { PageServerLoadEvent } from '../../$types';

export async function load({ locals: { auth } }: PageServerLoadEvent) {
    if (auth) {
        throw redirect(302, '/dashboard/')
    }
}

export const actions = {
    // login
    default: async ({ request, fetch, cookies }) => {
        const data = await request.formData()
        const email = String(data.get("email"))
        const password = String(data.get("password"))

        if (!email || !password)
            return fail(400, { missing: true });

        const reqInitOptions: RequestInit = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password,
            })
        }

        const res = await fetch(`http://${BASE_API_URI}/auth/login`, reqInitOptions)
        if (!res.ok) {
            let errors = {}
            try {
                const response = await res.json();
                errors = formatError(response.error);
            } catch (e) {
                errors = {}
            }
            return fail(400, { errors: errors });
        }

        const response = await res.json()
        const jwt = response?.jwt?.access_token
        cookies.set("jwt", jwt, {
            path: '/',
            maxAge: 60 * 60 * 24 * 365,
            httpOnly: false, // <-- if you want to read it in the browser
            secure: false,
            // sameSite: true,
        });

        throw redirect(303, "/dashboard")
    },
} satisfies Actions;
