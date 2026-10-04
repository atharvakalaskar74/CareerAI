// Multi-step Assessment Wizard Logic
document.addEventListener("DOMContentLoaded", function () {
  let currentStep = 1;
  const totalSteps = 7;

  const prevBtn = document.getElementById("wizardPrevBtn");
  const nextBtn = document.getElementById("wizardNextBtn");
  const submitBtn = document.getElementById("wizardSubmitBtn");
  const progressFill = document.getElementById("wizardProgressFill");
  const stepNumberBadge = document.getElementById("wizardStepNumber");

  function updateWizardUI() {
    // Show current step section and hide others
    for (let i = 1; i <= totalSteps; i++) {
      const stepElem = document.getElementById(`stepSection${i}`);
      const indicatorElem = document.getElementById(`stepIndicator${i}`);
      if (stepElem) {
        stepElem.style.display = i === currentStep ? "block" : "none";
      }
      if (indicatorElem) {
        if (i < currentStep) {
          indicatorElem.className = "wizard-step-item completed";
        } else if (i === currentStep) {
          indicatorElem.className = "wizard-step-item active";
        } else {
          indicatorElem.className = "wizard-step-item pending";
        }
      }
    }

    // Update buttons
    if (prevBtn) {
      prevBtn.style.display = currentStep > 1 ? "inline-flex" : "none";
    }
    if (nextBtn) {
      nextBtn.style.display = currentStep < totalSteps ? "inline-flex" : "none";
    }
    if (submitBtn) {
      submitBtn.style.display = currentStep === totalSteps ? "inline-flex" : "none";
    }

    // Update progress bar
    const percent = ((currentStep - 1) / (totalSteps - 1)) * 100;
    if (progressFill) {
      progressFill.style.width = `${percent}%`;
    }
    if (stepNumberBadge) {
      stepNumberBadge.textContent = `Step ${currentStep} of ${totalSteps}`;
    }

    // Scroll to top of wizard
    window.scrollTo({ top: 120, behavior: "smooth" });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      if (validateCurrentStep(currentStep)) {
        currentStep++;
        updateWizardUI();
      }
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      if (currentStep > 1) {
        currentStep--;
        updateWizardUI();
      }
    });
  }

  function validateCurrentStep(step) {
    if (step === 1) {
      const cgpa = document.getElementById("cgpa");
      if (cgpa && (parseFloat(cgpa.value) < 0 || parseFloat(cgpa.value) > 10 || isNaN(parseFloat(cgpa.value)))) {
        alert("Please enter a valid CGPA between 0.0 and 10.0");
        cgpa.focus();
        return false;
      }
    }
    return true;
  }

  // Live range badge listener
  const allSliders = document.querySelectorAll(".wizard-slider");
  allSliders.forEach(function (slider) {
    const valBadge = document.getElementById(slider.name + "_val");
    if (valBadge) {
      slider.addEventListener("input", function () {
        valBadge.textContent = slider.value + "/10";
      });
    }
  });

  // Pill toggle styling for checkboxes
  const interestChecks = document.querySelectorAll(".interest-checkbox");
  interestChecks.forEach(function (cb) {
    cb.addEventListener("change", function () {
      const label = cb.closest(".pill-label");
      if (label) {
        if (cb.checked) {
          label.classList.add("pill-selected");
        } else {
          label.classList.remove("pill-selected");
        }
      }
    });
  });

  updateWizardUI();
});
