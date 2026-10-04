// CareerAI Global Client Logic
document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = "0";
      alert.style.transition = "opacity 0.4s ease";
      setTimeout(function () {
        alert.remove();
      }, 400);
    }, 6000);
  });

  // Range slider live value synchronization for all standalone sliders
  const rangeInputs = document.querySelectorAll('input[type="range"]');
  rangeInputs.forEach(function (slider) {
    const targetBadge = document.getElementById(slider.id + "_val");
    if (targetBadge) {
      slider.addEventListener("input", function () {
        targetBadge.textContent = slider.value + "/10";
      });
    }
  });
});
