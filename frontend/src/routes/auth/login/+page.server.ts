import { fail, type Actions, redirect } from '@sveltejs/kit';
import { HOST } from '../../../config';

export const actions = {
    default: async ({ request, cookies }) => {

        const data = await request.formData()
        const email = data.get("email")
        const password = data.get("password")

        if (!email || !password)
            return fail(400, { missing: true });

        let res;
        try {
            res = await fetch(`http://${HOST}/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email.toString(),
                    password: password.toString(),
                }),
            })

            if (!res.ok) {
                const json = await res.json()
                console.log(json)
                throw {}
            }
        } catch (e) {
            return fail(400, { incorrect: true })
        }

        const json = await res.json()
        const jwt = json?.jwt?.access_token
        cookies.set("jwt", jwt,
            {
                path: '/',
                maxAge: 60 * 60 * 24 * 365,
                httpOnly: false, // <-- if you want to read it in the browser
                secure: false,
                // sameSite: true,

            }
        )
        return redirect(303, "/dashboard")
    },
} satisfies Actions;
