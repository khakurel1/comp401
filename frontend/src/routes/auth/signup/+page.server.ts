import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';
import { authStore } from '$store/auth';

export const actions = {
    default: async ({ request }) => {

        const data = await request.formData()

        const username = data.get("username")
        const email = data.get("email")
        const password = data.get("password")
        const confirm = data.get("confirm")

        if (!username || !email || !password || !confirm)
            return fail(400, { missing: true });

        if (password != confirm)
            return fail(400, { mismatch: true });

        try {
            const jwt = await authStore.signup(username.toString(), email.toString(), password.toString())
            console.log(jwt)
            return { success: true, jwt }
        } catch (e) {
            return fail(400, { incorrect: true });
        }
    },
} satisfies Actions;
