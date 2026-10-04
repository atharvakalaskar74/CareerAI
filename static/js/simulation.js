// What-If Career Simulator Interactive Engine
document.addEventListener("DOMContentLoaded", function () {
  const simSliders = document.querySelectorAll(".sim-slider");
  let debounceTimer = null;

  function runSimulation() {
    const baseline = {};
    const simulated = {};

    simSliders.forEach(function (slider) {
      const featName = slider.getAttribute("data-feature");
      const baseVal = parseFloat(slider.getAttribute("data-baseline"));
      const simVal = parseFloat(slider.value);

      baseline[featName] = baseVal;
      simulated[featName] = simVal;

      // Update slider value label
      const badge = document.getElementById(`val_${featName}`);
      if (badge) {
        badge.textContent = simVal + "/10";
      }

      // Visual diff indicator
      const diffTag = document.getElementById(`diff_${featName}`);
      if (diffTag) {
        const delta = simVal - baseVal;
        if (delta > 0) {
          diffTag.textContent = `(+${delta.toFixed(1)})`;
          diffTag.className = "sim-delta text-success";
        } else if (delta < 0) {
          diffTag.textContent = `(${delta.toFixed(1)})`;
          diffTag.className = "sim-delta text-danger";
        } else {
          diffTag.textContent = "(0.0)";
          diffTag.className = "sim-delta text-muted";
        }
      }
    });

    // Make AJAX call to backend prediction engine
    const loadingElem = document.getElementById("simLoading");
    if (loadingElem) loadingElem.style.display = "inline-block";

    fetch("/api/simulate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ baseline: baseline, simulated: simulated })
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (loadingElem) loadingElem.style.display = "none";
        if (data.status === "success") {
          updateSimulationResults(data);
        }
      })
      .catch(function (err) {
        if (loadingElem) loadingElem.style.display = "none";
        console.error("Simulation error:", err);
      });
  }

  function updateSimulationResults(data) {
    const afterResultsContainer = document.getElementById("simulatedResultsContainer");
    if (!afterResultsContainer) return;

    const after = data.after;
    const shifts = data.shifts;

    let html = `
      <div class="card mb-4" style="border-color: rgba(99, 102, 241, 0.4); background: rgba(99, 102, 241, 0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <span class="badge badge-primary">Simulated Top Prediction</span>
            <h2 class="card-title" style="font-size: 1.6rem; margin-top: 0.5rem;">${after.top_career}</h2>
            <p class="card-subtitle">Calculated using trained champion Machine Learning model.</p>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #818cf8;">${after.top_compatibility}%</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">Compatibility Score</div>
          </div>
        </div>
      </div>
      <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem;">Career Probability Differential Shifts</h3>
      <div style="display: flex; flex-direction: column; gap: 0.85rem;">
    `;

    shifts.forEach(function (s) {
      let shiftBadge = "";
      if (s.shift > 0) {
        shiftBadge = `<span class="badge badge-success">▲ +${s.shift}%</span>`;
      } else if (s.shift < 0) {
        shiftBadge = `<span class="badge badge-danger">▼ ${s.shift}%</span>`;
      } else {
        shiftBadge = `<span class="badge badge-warning">━ 0.0%</span>`;
      }

      html += `
        <div class="metric-box" style="text-align: left; padding: 1rem 1.25rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
            <span style="font-weight: 700; font-size: 1rem;">${s.career_title}</span>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <span style="font-size: 0.85rem; color: var(--text-muted);">Baseline: ${s.before_score}% → <strong>${s.after_score}%</strong></span>
              ${shiftBadge}
            </div>
          </div>
          <div class="progress-container" style="height: 10px;">
            <div class="progress-bar" style="width: ${s.after_score}%;"></div>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    afterResultsContainer.innerHTML = html;
  }

  // Attach input event with debounce
  simSliders.forEach(function (slider) {
    slider.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(runSimulation, 250);
    });
  });

  const resetBtn = document.getElementById("resetSimulationBtn");
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      simSliders.forEach(function (slider) {
        const baseVal = slider.getAttribute("data-baseline");
        slider.value = baseVal;
      });
      runSimulation();
    });
  }
});
