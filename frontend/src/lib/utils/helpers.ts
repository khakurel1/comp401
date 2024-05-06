import { BASE_API_URI } from "./constants";

function debounce(func: any, wait: number, immediate: boolean) {
    var timeout: number | null;
    return function() {
        var context = this, args = arguments;
        if (timeout) {
            clearTimeout(timeout);
        }
        timeout = setTimeout(function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        }, wait);
        if (immediate && !timeout) func.apply(context, args);
    };
}

export function formatError(obj: Object) {
    const errors = [];
    if (typeof obj === 'object' && obj !== null) {
        if (Array.isArray(obj)) {
            obj.forEach((error: Object) => {
                Object.keys(error).map((k) => {
                    errors.push({
                        error: error[k],
                        id: Math.random() * 1000
                    });
                });
            });
        } else {
            Object.keys(obj).map((k) => {
                errors.push({
                    error: obj[k],
                    id: Math.random() * 1000
                });
            });
        }
    } else {
        errors.push({
            error: obj.charAt(0).toUpperCase() + obj.slice(1),
            id: 0
        });
    }

    return errors;
}

export function get_user(jwt: string) {
    return fetch(`http://${BASE_API_URI}/auth/current_user/`, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer ' + jwt,
            'Content-Type': 'application/json'
        }),
    })

}

export function calculate_percent_Mark(
    x1: number,
    y1: number,
    x2: number,
    y2: number,
    percentage: number,
) {
    var slope = (y2 - y1) / (x2 - x1);
    var yIntercept = y1 - slope * x1;
    var totalDistance = Math.sqrt(
        Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2),
    );
    var distance3_1 = percentage * totalDistance;
    var x3_1 = x1 + (distance3_1 / totalDistance) * (x2 - x1);
    var y3_1 = slope * x3_1 + yIntercept;
    return { x: x3_1, y: y3_1 };
}

