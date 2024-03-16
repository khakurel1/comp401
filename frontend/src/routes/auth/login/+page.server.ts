import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';
import { authStore } from '$store/auth';

export const actions = {
    default: async ({ request }) => {

        const data = await request.formData()
        const email = data.get("email")
        const password = data.get("password")

        if (!email || !password)
            return fail(400, { missing: true });



        try {
            const jwt = await authStore.login(email.toString(), password.toString())
            return { success: true, jwt }
        } catch (e) {
            return fail(400, { incorrect: true });
        }
    },
} satisfies Actions;
