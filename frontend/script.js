document.addEventListener("DOMContentLoaded", function () {

    const BACKEND = "http://localhost:5000";

    // ================= LOGIN =================

    const loginBtn = document.getElementById("loginBtn");

    if (loginBtn) {

        loginBtn.addEventListener("click", async function () {

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const messageBox = document.getElementById("loginMessage");

            const selectedDevice = document.getElementById("deviceSelect")?.value || "Chrome";
            const selectedLocation = document.getElementById("locationSelect")?.value || "Home";

            let sessionId = localStorage.getItem("session_id");

            if (!sessionId) {
                sessionId = "S_" + Date.now();
                localStorage.setItem("session_id", sessionId);
            }

            console.log("Using session:", sessionId);

            // LOGIN_ATTEMPT
            await fetch(`${BACKEND}/log-event`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: sessionId,
                    user_id: username || "USER1",
                    event_type: "LOGIN_ATTEMPT"
                })
            });

            // Wrong password
            if (password !== "1234") {

                await fetch(`${BACKEND}/log-event`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        session_id: sessionId,
                        user_id: username || "USER1",
                        event_type: "LOGIN_FAILURE"
                    })
                });

                messageBox.textContent = "Invalid password. Try again.";
                return;
            }

            // LOGIN_SUCCESS
            await fetch(`${BACKEND}/log-event`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: sessionId,
                    user_id: username || "USER1",
                    event_type: "LOGIN_SUCCESS",
                    metadata: {
                        user_agent: selectedDevice,
                        location: selectedLocation
                    }
                })
            });

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

    async function logDashboardEvent(eventType) {
        const sessionId = localStorage.getItem("session_id");
        if (!sessionId) return;

        await fetch(`${BACKEND}/log-event`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                session_id: sessionId,
                user_id: "USER1",
                event_type: eventType
            })
        });
    }

    async function fetchRisk() {
        const sessionId = localStorage.getItem("session_id");
        if (!sessionId) return;

        const response = await fetch(`${BACKEND}/risk/${sessionId}`);
        const data = await response.json();

        const riskBox = document.getElementById("riskDisplay");
        if (!riskBox) return;

        if (data.risk) {
            riskBox.textContent = JSON.stringify(data.risk, null, 2);

            if (data.risk.risk_class === "HIGH") {
                riskBox.style.backgroundColor = "#ffe6e6";
                riskBox.style.color = "red";
            } else if (data.risk.risk_class === "MEDIUM") {
                riskBox.style.backgroundColor = "#fff4cc";
                riskBox.style.color = "orange";
            } else {
                riskBox.style.backgroundColor = "#e6ffe6";
                riskBox.style.color = "green";
            }
        }
    }

    // Core Buttons

    if (viewBtn) {
        viewBtn.addEventListener("click", async function () {
            await logDashboardEvent("VIEW_DASHBOARD");
            await fetchRisk();
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener("click", async function () {

            if (normalModeDelay) {
                await new Promise(resolve => setTimeout(resolve, 3000));
            }

            await logDashboardEvent("DOWNLOAD_STATEMENT");
            await fetchRisk();
        });
    }

    if (passwordBtn) {
        passwordBtn.addEventListener("click", async function () {

            if (normalModeDelay) {
                await new Promise(resolve => setTimeout(resolve, 3000));
            }

            await logDashboardEvent("CHANGE_PASSWORD");
            await fetchRisk();
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

            await logDashboardEvent("DOWNLOAD_STATEMENT");
            await logDashboardEvent("CHANGE_PASSWORD");

            await fetchRisk();

            alert("Immediate attack pattern executed.");
        });
    }

    if (rapidActionBtn) {
        rapidActionBtn.addEventListener("click", async function () {

            normalModeDelay = false;

            for (let i = 0; i < 3; i++) {
                await logDashboardEvent("DOWNLOAD_STATEMENT");
            }

            await fetchRisk();

            alert("Rapid burst executed.");
        });
    }

});
