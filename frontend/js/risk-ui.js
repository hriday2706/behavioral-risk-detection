export function updateRiskUI(data) {

    const riskBar = document.getElementById("riskBar");
    const riskText = document.getElementById("riskText");
    const reasonsBox = document.getElementById("riskReasons");

    const sensitiveButtons = document.querySelectorAll(".sensitive");

    if (!data) return;

    const score = data.risk_score;
    const riskClass = data.risk_class;
    const alertBox = document.getElementById("securityAlert");

    if (riskClass === "HIGH") {
        alertBox.style.display = "block";
    } else {
        alertBox.style.display = "none";
    }

    
    // Update text
    riskText.textContent = `Risk: ${riskClass} (${score})`;

    // Update progress bar
    riskBar.style.width = Math.min(score, 100) + "%";

    if (riskClass === "HIGH") {
        riskBar.style.background = "red";
    } else if (riskClass === "MEDIUM") {
        riskBar.style.background = "orange";
    } else {
        riskBar.style.background = "green";
    }

    // Show reasons
    reasonsBox.innerHTML = "";
    data.reasons.forEach(reason => {
        const p = document.createElement("p");
        p.textContent = "• " + reason;
        reasonsBox.appendChild(p);
    });

    // 🔐 AUTO LOCK SENSITIVE BUTTONS
    if (riskClass === "HIGH") {
        sensitiveButtons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = "0.5";
        });
    } else {
        sensitiveButtons.forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = "1";
        });
    }
}
