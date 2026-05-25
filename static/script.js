// Strict sequence array ensuring synchronization with Python's expected feature slots
const featureSequence = ['V1', 'V2', 'V3', 'V4', 'V5', 'V7', 'V9', 'V10', 'V11', 'V12', 'V14', 'V16', 'V17', 'V18'];
const container = document.getElementById('inputContainer');

// Construct layout controls dynamically
featureSequence.forEach(feat => {
    const fieldWrapper = document.createElement('div');
    fieldWrapper.className = 'form-row';
    fieldWrapper.innerHTML = `
        <label for="${feat}">Component Variable ${feat}:</label>
        <input type="number" id="${feat}" name="${feat}" step="any" required placeholder="0.00">
    `;
    container.appendChild(fieldWrapper);
});

// Listener interception
document.getElementById('fraudPredictionForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const submitBtn = document.getElementById('submitButton');
    const outputCard = document.getElementById('outputCard');
    const outputText = document.getElementById('outputText');
    
    // Process input text nodes securely into Float values
    const featureArrayPayload = [];
    for (const key of featureSequence) {
        const rawValue = parseFloat(document.getElementById(key).value);
        if (isNaN(rawValue)) {
            alert(`Input entry for "${key}" must be a real numerical structure.`);
            return;
        }
        featureArrayPayload.push(rawValue);
    }

    // Set UI to running/loading configuration
    submitBtn.disabled = true;
    submitBtn.textContent = 'Running Inference Machine...';
    outputCard.className = 'output hidden';

    try {
        // Direct absolute fetch pipeline directly to the external Flask instance URL
        const networkCall = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ features: featureArrayPayload })
        });

        const jsonResponse = await networkCall.json();
        outputCard.className = 'output';
        
        if (!networkCall.ok) {
            outputCard.classList.add('status-fraud');
            outputText.innerHTML = `<strong>Inference Runtime Error:</strong> ${jsonResponse.error || 'Server rejected sequence.'}`;
            return;
        }

        // Branching style updates based on response state
        if (jsonResponse.is_fraud) {
            outputCard.classList.add('status-fraud');
            outputText.innerHTML = `<strong>High Suspicion:</strong> Anomalous Fraud Pattern Flagged.<br><small>Confidence Level: ${(jsonResponse.fraud_probability * 100).toFixed(3)}% Probability</small>`;
        } else {
            outputCard.classList.add('status-legit');
            outputText.innerHTML = `<strong>Authorized:</strong> Standard Transaction Vector.<br><small>Risk Factor: ${(jsonResponse.fraud_probability * 100).toFixed(3)}% Probability</small>`;
        }
        
    } catch (networkFault) {
        outputCard.className = 'output';
        outputCard.classList.add('status-fraud');
        outputText.innerHTML = `<strong>Network Exception:</strong> Connection refused. Verify that your Flask runtime environment is listening on Port 5000.`;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Analyze Transaction Parameters';
    }
});