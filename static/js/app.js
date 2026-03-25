document.getElementById('urlForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const urlInput = document.getElementById('urlInput');
    const resultDiv = document.getElementById('result');
    const url = urlInput.value.trim();
    if (!url) return;

    // Show loading state
    resultDiv.className = 'result hidden';
    resultDiv.textContent = 'Analyzing...';
    resultDiv.classList.remove('hidden');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        if (data.error) {
            resultDiv.textContent = data.error;
            resultDiv.className = 'result hidden';
            return;
        }
        const { is_phishing, reasons, confidence } = data;
        const status = is_phishing ? 'Phishing' : 'Safe';
        const badgeClass = is_phishing ? 'phish' : 'safe';
        let html = `<h3 class="${badgeClass}">${status}</h3>`;
        html += `<p>Confidence: ${(confidence * 100).toFixed(0)}%</p>`;
        if (is_phishing && reasons.length) {
            html += '<ul>' + reasons.map(r => `<li>${r}</li>`).join('') + '</ul>';
        }
        resultDiv.innerHTML = html;
        resultDiv.className = `result ${badgeClass}`;
    } catch (err) {
        resultDiv.textContent = 'Error contacting server.';
        resultDiv.className = 'result hidden';
    }
});
