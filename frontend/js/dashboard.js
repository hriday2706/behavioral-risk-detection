// ================= DASHBOARD CONTROLLER =================

import { logEvent } from "./api.js";
import { updateRiskUI } from "./risk-ui.js";
import { getSession } from "./session.js";

// Ensure session exists
if (!getSession()) {
    window.location.href = "index.html";
}

// ================= BUTTON REFERENCES =================

const viewBtn = document.getElementById("viewBtn");
const downloadBtn = document.getElementById("downloadBtn");
const passwordBtn = document.getElementById("passwordBtn");

const normalModeBtn = document.getElementById("normalModeBtn");
const attackModeBtn = document.getElementById("attackModeBtn");
const rapidActionBtn = document.getElementById("rapidActionBtn");

let normalModeDelay = true;

// ================= CORE ACTION HANDLER =================

async function handleEvent(eventType) {
    const riskData = await logEvent(eventType);

    if (riskData) {
        updateRiskUI(riskData);
        addToTimeline(eventType);
    }
}

function addToTimeline(eventType) {
    const feed = document.getElementById("activityFeed");
    if (!feed) return;

    const li = document.createElement("li");
    li.textContent = new Date().toLocaleTimeString() + " — " + eventType;

    feed.prepend(li);
}

// ================= CORE ACTIONS =================

// View Dashboard
if (viewBtn) {
    viewBtn.addEventListener("click", async () => {
        await handleEvent("VIEW_DASHBOARD");
    });
}

// Download Statement (Sensitive)
if (downloadBtn) {
    downloadBtn.addEventListener("click", async () => {

        if (normalModeDelay) {
            await new Promise(resolve => setTimeout(resolve, 3000));
        }

        await handleEvent("DOWNLOAD_STATEMENT");
    });
}

// Change Password (Sensitive)
if (passwordBtn) {
    passwordBtn.addEventListener("click", async () => {

        if (normalModeDelay) {
            await new Promise(resolve => setTimeout(resolve, 3000));
        }

        await handleEvent("CHANGE_PASSWORD");
    });
}

// ================= BEHAVIOR MODES =================

if (normalModeBtn) {
    normalModeBtn.addEventListener("click", () => {
        normalModeDelay = true;
        alert("Normal browsing mode activated.");
    });
}

if (attackModeBtn) {
    attackModeBtn.addEventListener("click", async () => {

        normalModeDelay = false;

        await handleEvent("BURST_ACTION");
        await handleEvent("DOWNLOAD_STATEMENT");
        await handleEvent("CHANGE_PASSWORD");

        alert("Immediate attack pattern executed.");
    });
}

if (rapidActionBtn) {
    rapidActionBtn.addEventListener("click", async () => {

        normalModeDelay = false;

        await handleEvent("BURST_ACTION");

        alert("Rapid burst executed.");
    });
}
const transactionsBtn = document.getElementById("transactionsBtn");
const profileBtn = document.getElementById("profileBtn");
const loanBtn = document.getElementById("loanBtn");
const transferBtn = document.getElementById("transferBtn");

if (transactionsBtn) {
    transactionsBtn.addEventListener("click", () => handleEvent("VIEW_TRANSACTIONS"));
}

if (profileBtn) {
    profileBtn.addEventListener("click", () => handleEvent("VIEW_PROFILE"));
}

if (loanBtn) {
    loanBtn.addEventListener("click", () => handleEvent("VIEW_LOANS"));
}

if (transferBtn) {
    transferBtn.addEventListener("click", () => handleEvent("TRANSFER_FUNDS"));
}
