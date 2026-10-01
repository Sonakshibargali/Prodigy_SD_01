/**
 * Temperature Converter Client Script
 * Handles input validation, API communication, and dynamic UI updates.
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('converter-form');
    const tempInput = document.getElementById('temp-input');
    const unitSelect = document.getElementById('unit-select');
    const clearBtn = document.getElementById('clear-btn');
    const convertBtn = document.getElementById('convert-btn');
    
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const inputSummary = document.getElementById('input-summary');

    // Physical absolute zero constants for client-side quick validation
    const ABSOLUTE_ZERO = {
        C: -273.15,
        F: -459.67,
        K: 0.0
    };

    /**
     * Display error message in the alert container.
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.classList.add('show');
        resultsSection.classList.remove('show');
    }

    /**
     * Clear error alert.
     */
    function hideError() {
        errorAlert.classList.remove('show');
        errorMessage.textContent = '';
    }

    /**
     * Validate user input on client side.
     * Returns { valid: boolean, error?: string, numericValue?: number }
     */
    function validateClientInput(rawVal, unit) {
        if (!rawVal || rawVal.trim() === '') {
            return { valid: false, error: 'Please enter a temperature value.' };
        }

        const num = Number(rawVal.trim());
        if (isNaN(num)) {
            return { valid: false, error: 'Invalid temperature. Please enter a valid number.' };
        }

        if (unit === 'K' && num < ABSOLUTE_ZERO.K) {
            return { valid: false, error: 'Kelvin temperature cannot be below absolute zero (0.00 K).' };
        }

        if (unit === 'C' && num < ABSOLUTE_ZERO.C) {
            return { valid: false, error: 'Celsius temperature cannot be below absolute zero (-273.15 °C).' };
        }

        if (unit === 'F' && num < ABSOLUTE_ZERO.F) {
            return { valid: false, error: 'Fahrenheit temperature cannot be below absolute zero (-459.67 °F).' };
        }

        return { valid: true, numericValue: num };
    }

    /**
     * Render conversion results cards.
     */
    function renderResults(data) {
        inputSummary.textContent = `From ${data.input.formatted} ${data.input.symbol}`;
        
        // Clear previous results grid
        resultsGrid.innerHTML = '';

        data.results.forEach((item) => {
            const card = document.createElement('div');
            card.className = 'result-card';

            const label = document.createElement('span');
            label.className = 'result-label';
            label.textContent = item.name;

            const valueGroup = document.createElement('div');
            valueGroup.className = 'result-value-group';

            const valueSpan = document.createElement('span');
            valueSpan.className = 'result-value';
            valueSpan.textContent = item.formatted;

            const symbolSpan = document.createElement('span');
            symbolSpan.className = 'result-symbol';
            symbolSpan.textContent = item.symbol;

            valueGroup.appendChild(valueSpan);
            valueGroup.appendChild(symbolSpan);

            card.appendChild(label);
            card.appendChild(valueGroup);
            resultsGrid.appendChild(card);
        });

        resultsSection.classList.add('show');
    }

    /**
     * Handle form submission via AJAX / Fetch API.
     */
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();

        const rawVal = tempInput.value;
        const unit = unitSelect.value;

        // Perform client-side check
        const validation = validateClientInput(rawVal, unit);
        if (!validation.valid) {
            showError(validation.error);
            tempInput.focus();
            return;
        }

        // Set loading state on button
        const originalBtnText = convertBtn.innerHTML;
        convertBtn.disabled = true;
        convertBtn.innerHTML = '<span class="btn-text">Converting...</span>';

        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    temperature: validation.numericValue,
                    unit: unit
                })
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                const err = result.error || 'Conversion failed. Please try again.';
                showError(err);
                return;
            }

            renderResults(result.data);
        } catch (networkError) {
            showError('Unable to connect to the server. Please check your connection.');
        } finally {
            convertBtn.disabled = false;
            convertBtn.innerHTML = originalBtnText;
        }
    });

    /**
     * Clear / Reset Button handler.
     */
    clearBtn.addEventListener('click', () => {
        tempInput.value = '';
        unitSelect.value = 'C';
        hideError();
        resultsSection.classList.remove('show');
        tempInput.focus();
    });

    /**
     * Dismiss error alert as soon as the user starts typing.
     */
    tempInput.addEventListener('input', () => {
        if (errorAlert.classList.contains('show')) {
            hideError();
        }
    });

    // Auto-focus input on page load
    tempInput.focus();
});
