import { get, writable } from "svelte/store";

// response
//  {
//   "status": "success",
//   "jwt": {
//     "access_token": "token_123"
//   }
// }
//
//
export interface AuthStore {
    login: (email: string, password: string) => Promise<string>
    signup: (username: string, email: string, password: string) => Promise<string>
    refresh: () => void
    logout: () => void
    value: () => string
}

export function createAuthStore() {

    let g_email, g_password: string;
    const jwt = writable("")

    // subscribe((data) => {
    //     window.localStorage.setItem("jwt", data)
    // })


    async function signup(username: string, email: string, password: string) {
        g_email = email
        g_password = password
        const res = await fetch("http://localhost:8081/auth/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        })
        if (res.status == 422 || res.status == 404) { // 422 validation error, 404 not found error
            throw await res.json()
        }

        const data = await res.json()
        jwt.set(data?.jwt?.access_token)
        return data?.jwt?.access_token
    }

    async function login(email: string, password: string) {
        g_email = email
        g_password = password
        const res = await fetch("http://localhost:8081/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        })
        if (res.status == 422 || res.status == 404) { // 422 validation error, 404 not found error
            throw await res.json()
        }

        const data = await res.json()
        jwt.set(data?.jwt?.access_token)
        return data?.jwt?.access_token
    }

    async function refresh() {
        // if (window.localStorage.getItem("jwt") == null) {
        //     throw "user not logged in! refresh failed."
        // }

        const res = await fetch("localhost:8081/auth/login")
        if (res.status != 200) { // 422 validation error, 404 not found error
            return
        }
        const data = await res.json()
        jwt.set(data?.jwt?.access_token)
    }

    function logout() {
        jwt.set("")
    }

    function value() {
        console.log("getting value")
        return get(jwt)
    }

    return {
        login, signup, refresh, logout, value
    } as AuthStore
}

export const authStore = createAuthStore()
