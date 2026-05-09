import type {Risiko, RisikoCreate} from "../types";

const BASE_URL = "/api";

export class ApiValidationError extends Error {
    status: number;
    fieldErrors: Record<string, string>;

    constructor(message: string, status: number, fieldErrors: Record<string, string>) {
        super(message);
        this.status = status;
        this.fieldErrors = fieldErrors;
    }
}

export async function fetchRisiken(params?: {
    risikoart?: string;
    status?: string;
}): Promise<Risiko[]> {
    const url = new URL(`${BASE_URL}/risiken`, window.location.origin);
    if (params?.risikoart) url.searchParams.set("risikoart", params.risikoart);
    if (params?.status) url.searchParams.set("status", params.status);

    const response = await fetch(url.toString().replace(window.location.origin, ""), {
        headers: {Accept: "application/json"},
    });

    if (!response.ok) {
        throw new Error(`Fehler beim Laden (${response.status})`);
    }
    return (await response.json()) as Risiko[];
}

export async function createRisiko(payload: RisikoCreate): Promise<Risiko> {
    const response = await fetch(`${BASE_URL}/risiken`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        let message = `Fehler beim Anlegen (${response.status})`;
        const fieldErrors: Record<string, string> = {};
        try {
            const body = await response.json();
            if (typeof body?.message === "string") message = body.message;
            else if (typeof body?.detail === "string") message = body.detail;
            if (Array.isArray(body?.errors)) {
                for (const e of body.errors) {
                    if (e && typeof e.field === "string" && typeof e.message === "string") {
                        fieldErrors[e.field] = e.message;
                    }
                }
            }
        } catch {
            // body kein JSON – ignorieren
        }
        if (response.status >= 400 && response.status < 500) {
            throw new ApiValidationError(message, response.status, fieldErrors);
        }
        throw new Error(message);
    }

    return (await response.json()) as Risiko;
}
