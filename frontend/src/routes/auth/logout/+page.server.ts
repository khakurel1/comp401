import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from '../../$types';

export const load: PageServerLoad = ({ cookies }) => {
    cookies.delete("jwt",
        {
            path: '/',
            maxAge: 60 * 60 * 24 * 365,
            httpOnly: false, // <-- if you want to read it in the browser
        }
    )
    return redirect(301, "/auth/login")
};
