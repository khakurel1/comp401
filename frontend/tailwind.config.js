/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './src/*.{html,js,svelte,ts}'
        , './src/**/*.{html,js,svelte,ts}'
    ],
    theme: {
        extend: {
            colors: {
                "brown": "#444444",
            }
        },
    },
    plugins: [require("daisyui")],
}

