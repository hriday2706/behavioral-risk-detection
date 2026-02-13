// session.js

export function createSession() {
    const sessionId = "S_" + Date.now();
    localStorage.setItem("session_id", sessionId);
    return sessionId;
}

export function getSession() {
    return localStorage.getItem("session_id");
}

export function clearSession() {
    localStorage.removeItem("session_id");
}
