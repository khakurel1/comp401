import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from "vite";

export default defineConfig(() => {
    // const env = loadEnv('', process.cwd());
    return {
        plugins: [sveltekit()],
        build: {
            sourcemap: true,
        },
        // define: {
        //     VITE_BACKEND_URL: env.VITE_BACKEND_URL,
        // }
    }
}
);
