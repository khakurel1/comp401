import { HOST } from "../config"

interface APIError {
    status: number,
    body: any
}

async function signup(username: string, email: string, password: string) {
    const res = await fetch(`http://${HOST}/auth/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
    })
    if (!res.ok) {
        const data = await res.json()
        throw {
            status: res.status,
            body: data.detail,
        }
    }

    const data = await res.json()
    return data?.jwt?.access_token
}


async function login(email: string, password: string) {
    const res = await fetch(`http://${HOST}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    })
    if (!res.ok) {
        const data = await res.json()
        throw {
            status: res.status,
            body: data.detail,
        }
    }

    const data = await res.json()
    return data?.jwt?.access_token
}

export {
    signup, login, type APIError
}
