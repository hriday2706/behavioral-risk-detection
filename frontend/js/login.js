import { createSession } from "./session.js";
import { logEvent } from "./api.js";

document.addEventListener("DOMContentLoaded", function () {

    const loginBtn = document.getElementById("loginBtn");

    if (!loginBtn) return;

    loginBtn.addEventListener("click", async function () {

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const messageBox = document.getElementById("loginMessage");

        const selectedDevice = document.getElementById("deviceSelect").value;
        const selectedLocation = document.getElementById("locationSelect").value;
        const selectedTimeMode = document.getElementById("timeMode").value;

        // Always create fresh session
        const sessionId = createSession();

        // LOGIN ATTEMPT
        await logEvent("LOGIN_ATTEMPT");

        // Wrong password
        if (password !== "1234") {
            await logEvent("LOGIN_FAILURE");
            messageBox.textContent = "Invalid password.";
            return;
        }

        // Optional simulated anomalies
        if (selectedDevice !== "Chrome") {
            await logEvent("NEW_DEVICE");
        }

        if (selectedLocation === "Foreign") {
            await logEvent("TRAVEL_ANOMALY");
        }

        if (selectedTimeMode === "odd") {
            await logEvent("ODD_LOGIN_TIME");
        }

        // LOGIN SUCCESS
        await logEvent("LOGIN_SUCCESS");

        messageBox.textContent = "";
        window.location.href = "dashboard.html";
    });
});
