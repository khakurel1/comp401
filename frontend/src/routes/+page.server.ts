import { redirect } from '@sveltejs/kit';
import type {  PageServerLoad } from './$types';

export const load: PageServerLoad = () => {
   throw redirect(307, '/dashboard');
};

// export const ssr = false;
// export const csr = true;
// export const prerender = false;
// export const trailingSlash = 'always';
