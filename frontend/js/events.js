document.addEventListener("DOMContentLoaded", function () {

    const BACKEND = "http://localhost:5000";

    // ================= UI RISK UPDATE =================

    function updateRiskUI(data) {
        const riskBox = document.getElementById("riskDisplay");
        if (!riskBox) return;

        riskBox.textContent = JSON.stringify(data, null, 2);

        if (data.risk_class === "HIGH") {
            riskBox.style.backgroundColor = "#ffe6e6";
            riskBox.style.color = "red";
        } else if (data.risk_class === "MEDIUM") {
            riskBox.style.backgroundColor = "#fff4cc";
            riskBox.style.color = "orange";
        } else {
            riskBox.style.backgroundColor = "#e6ffe6";
            riskBox.style.color = "green";
        }
    }

    async function logEvent(eventType, metadata = {}) {
        const sessionId = localStorage.getItem("session_id");
        if (!sessionId) return;

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

        const riskData = await response.json();
        updateRiskUI(riskData);
    }

    // ================= LOGIN =================

    const loginBtn = document.getElementById("loginBtn");

    if (loginBtn) {

        loginBtn.addEventListener("click", async function () {

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const messageBox = document.getElementById("loginMessage");

            const selectedDevice = document.getElementById("deviceSelect")?.value || "Chrome";
            const selectedLocation = document.getElementById("locationSelect")?.value || "Home";
            const timeMode = document.getElementById("timeMode")?.value || "normal";

            // Always fresh session
            const sessionId = "S_" + Date.now();
            localStorage.setItem("session_id", sessionId);

            // LOGIN ATTEMPT
            await logEvent("LOGIN_ATTEMPT");

            // RAPID RETRY DETECTION
            let lastAttempt = localStorage.getItem("last_attempt_time");
            let nowMs = Date.now();

            if (lastAttempt && (nowMs - lastAttempt) < 2000) {
                await logEvent("RAPID_RETRY");
            }

            localStorage.setItem("last_attempt_time", nowMs);

            // WRONG PASSWORD
            if (password !== "1234") {
                await logEvent("LOGIN_FAILURE");
                messageBox.textContent = "Invalid password.";
                return;
            }

            // LOGIN SUCCESS
            await logEvent("LOGIN_SUCCESS");

            // -------- Emit anomaly signals --------

            if (selectedDevice !== "Chrome") {
                await logEvent("NEW_DEVICE");
            }

            if (selectedLocation === "Foreign") {
                await logEvent("TRAVEL_ANOMALY");
            }

            if (timeMode === "odd") {
                await logEvent("ODD_LOGIN_TIME");
            }

            messageBox.textContent = "";
            window.location.href = "dashboard.html";
        });
    }

    // ================= DASHBOARD =================

    const viewBtn = document.getElementById("viewBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const passwordBtn = document.getElementById("passwordBtn");

    const normalModeBtn = document.getElementById("normalModeBtn");
    const attackModeBtn = document.getElementById("attackModeBtn");
    const rapidActionBtn = document.getElementById("rapidActionBtn");

    let normalModeDelay = true;

    if (viewBtn) {
        viewBtn.addEventListener("click", async function () {
            await logEvent("VIEW_DASHBOARD");
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener("click", async function () {

            if (normalModeDelay) {
                await new Promise(resolve => setTimeout(resolve, 3000));
            }

            await logEvent("DOWNLOAD_STATEMENT");
        });
    }

    if (passwordBtn) {
        passwordBtn.addEventListener("click", async function () {

            if (normalModeDelay) {
                await new Promise(resolve => setTimeout(resolve, 3000));
            }

            await logEvent("CHANGE_PASSWORD");
        });
    }

    // ================= BEHAVIOR SIMULATION =================

    if (normalModeBtn) {
        normalModeBtn.addEventListener("click", function () {
            normalModeDelay = true;
            alert("Normal browsing mode activated.");
        });
    }

    if (attackModeBtn) {
        attackModeBtn.addEventListener("click", async function () {
            normalModeDelay = false;

            await logEvent("BURST_ACTION");
            await logEvent("DOWNLOAD_STATEMENT");
            await logEvent("CHANGE_PASSWORD");

            alert("Attack pattern executed.");
        });
    }

    if (rapidActionBtn) {
        rapidActionBtn.addEventListener("click", async function () {
            normalModeDelay = false;

            await logEvent("BURST_ACTION");

            alert("Rapid burst executed.");
        });
    }

});
