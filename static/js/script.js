// DOM Elements
const textInput = document.getElementById('text-input');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const charCount = document.getElementById('char-count');
const resultsSection = document.getElementById('results-section');
const resultsContent = document.getElementById('results-content');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const closeResultsBtn = document.getElementById('close-results');
const exampleBtns = document.querySelectorAll('.example-btn');

// Character counter
if (textInput && charCount) {
    textInput.addEventListener('input', () => {
        charCount.textContent = textInput.value.length;
    });
}

// Example buttons
exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const exampleText = btn.dataset.example;
        textInput.value = exampleText;
        charCount.textContent = exampleText.length;
    });
});

// Clear button
if (clearBtn) {
    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        charCount.textContent = '0';
        hideResults();
        hideError();
    });
}

// Close results
if (closeResultsBtn) {
    closeResultsBtn.addEventListener('click', hideResults);
}

// Analyze button
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            showError('Please enter some text to analyze.');
            return;
        }
        await analyzeText(text);
    });
}

// Main analysis function
async function analyzeText(text) {
    try {
        hideResults();
        hideError();
        loading.classList.remove('hidden');
        analyzeBtn.disabled = true;

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        loading.classList.add('hidden');
        analyzeBtn.disabled = false;

        if (!response.ok || !data.success) {
            showError(data.error || 'An error occurred during analysis.');
            return;
        }

        displayResults(data.result);

    } catch (error) {
        console.error('Error:', error);
        loading.classList.add('hidden');
        analyzeBtn.disabled = false;
        showError('Failed to connect to the server. Please try again.');
    }
}

// Display results
function displayResults(result) {
    let html = '';

    if (result.is_neutral) {
        html = `
            <div class="neutral-result">
                <div class="neutral-icon">✅</div>
                <h3>No Strong Bias Detected!</h3>
                <p>The text appears relatively neutral or objective.</p>
                <p style="margin-top: 1rem;">Word count: ${result.word_count}</p>
            </div>
        `;
    } else {
        html = `
            <div class="score-display">
                <div class="score-number">${result.overall_score}%</div>
                <div class="score-label">Overall Bias Score</div>
                <p style="margin-top: 0.5rem;">
                    Word count: ${result.word_count} | Found ${result.biases.length} type(s) of bias
                </p>
            </div>
            <div class="bias-list-container">
                <h3>Detected Biases:</h3>
                ${result.biases.map(bias => createBiasCard(bias)).join('')}
            </div>
        `;
    }

    resultsContent.innerHTML = html;
    resultsSection.classList.remove('hidden');
}

// Create bias card
function createBiasCard(bias) {
    const uniqueKeywords = [...new Set(bias.matches)];
    let scoreColor = '#5E6623';
    if (bias.score > 5) scoreColor = '#CB7885';
    if (bias.score > 10) scoreColor = '#893941';

    return `
        <div class="bias-item">
            <div class="bias-header">
                <span class="bias-name">${bias.type}</span>
                <span class="bias-score" style="background: ${scoreColor};">
                    ${bias.score}% intensity
                </span>
            </div>
            <p class="bias-explanation">${bias.explanation}</p>
            <div class="bias-matches">
                <strong>Found (${bias.count}):</strong>
                ${uniqueKeywords.map(keyword => 
                    `<span class="keyword-tag">${keyword}</span>`
                ).join('')}
            </div>
        </div>
    `;
}

// Show error
function showError(message) {
    errorMessage.textContent = `⚠️ ${message}`;
    errorMessage.classList.remove('hidden');
    setTimeout(hideError, 5000);
}

// Hide error
function hideError() {
    errorMessage.classList.add('hidden');
}

// Hide results
function hideResults() {
    resultsSection.classList.add('hidden');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (textInput) textInput.focus();
});
