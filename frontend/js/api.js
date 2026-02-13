// ================= API LAYER =================

import { getSession } from "./session.js";

const BACKEND = "http://localhost:5000";

export async function logEvent(eventType, metadata = {}) {
    const sessionId = getSession();

    if (!sessionId) {
        console.error("No active session.");
        return null;
    }

    try {
        const response = await fetch(`${BACKEND}/log-event`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId,
                user_id: "USER1",
                event_type: eventType,
                timestamp: Date.now() / 1000,
                metadata: metadata
            })
        });

        const data = await response.json();
        return data;

    } catch (error) {
        console.error("API Error:", error);
        return null;
    }
}
