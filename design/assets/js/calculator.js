/**
 * Search Economics & AEO Risk Calculator
 */
document.addEventListener('DOMContentLoaded', () => {
  const trafficInput = document.getElementById('calc-traffic');
  const valueInput = document.getElementById('calc-value');
  const crInput = document.getElementById('calc-cr');
  const leakInput = document.getElementById('calc-leak');

  const trafficVal = document.getElementById('val-traffic');
  const valueVal = document.getElementById('val-value');
  const crVal = document.getElementById('val-cr');
  const leakVal = document.getElementById('val-leak');

  const monthlyRes = document.getElementById('calc-result-monthly');
  const annualRes = document.getElementById('calc-result-annual');
  const leadsRes = document.getElementById('calc-result-leads');

  const presets = document.querySelectorAll('.calc-btn');

  const presetData = {
    hvac: { traffic: 25000, value: 800, cr: 15.0, leak: 25.0 },
    saas: { traffic: 15000, value: 2500, cr: 3.0, leak: 35.0 },
    ecom: { traffic: 60000, value: 85, cr: 2.5, leak: 20.0 }
  };

  function formatMoney(num) {
    return '$' + Math.round(num).toLocaleString();
  }

  function calculate() {
    if (!trafficInput || !valueInput || !crInput || !leakInput) return;

    const traffic = parseFloat(trafficInput.value);
    const value = parseFloat(valueInput.value);
    const cr = parseFloat(crInput.value) / 100;
    const leak = parseFloat(leakInput.value) / 100;

    trafficVal.textContent = Math.round(traffic).toLocaleString();
    valueVal.textContent = '$' + Math.round(value).toLocaleString();
    crVal.textContent = (cr * 100).toFixed(1) + '%';
    leakVal.textContent = (leak * 100).toFixed(1) + '%';

    // Calculation:
    // Potential conversions without leakage = traffic * cr
    // Conversions lost = potential * leak
    // Monthly revenue leakage = lost conversions * LTV/Ticket
    const potentialConversions = traffic * cr;
    const lostConversions = potentialConversions * leak;
    const monthlyLeakage = lostConversions * value;
    const annualLeakage = monthlyLeakage * 12;

    if (monthlyRes) monthlyRes.textContent = formatMoney(monthlyLeakage);
    if (annualRes) annualRes.textContent = formatMoney(annualLeakage);
    if (leadsRes) leadsRes.textContent = Math.round(lostConversions).toLocaleString() + ' leads';
  }

  presets.forEach(btn => {
    btn.addEventListener('click', () => {
      presets.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const data = presetData[btn.dataset.preset];
      if (data) {
        trafficInput.value = data.traffic;
        valueInput.value = data.value;
        crInput.value = data.cr;
        leakInput.value = data.leak;
        calculate();
      }
    });
  });

  [trafficInput, valueInput, crInput, leakInput].forEach(inp => {
    if (inp) inp.addEventListener('input', calculate);
  });

  calculate();
});
