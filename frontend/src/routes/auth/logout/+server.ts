import { json, redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { authStore } from '$store/auth';

export const GET: RequestHandler = () => {
    console.log("here")
    authStore.logout()
    return redirect(301, "/auth/login")
};
