// Theme Toggle
const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    body.classList.remove('light-mode');
    body.classList.add('dark-mode');
    themeSwitch.checked = true;
}

themeSwitch.addEventListener('change', (e) => {
    if (e.target.checked) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
    }
});

// Model Selection
const modelTabs = document.querySelectorAll('.model-tab');
const predictionForms = document.querySelectorAll('.prediction-form');

modelTabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
        const targetForm = e.target.closest('.model-tab').dataset.form;
        
        // Update active tab
        modelTabs.forEach(t => t.classList.remove('active'));
        e.target.closest('.model-tab').classList.add('active');
        
        // Show target form
        predictionForms.forEach(form => {
            if (form.id === targetForm) {
                form.style.display = 'block';
            } else {
                form.style.display = 'none';
            }
        });
    });
});

// Form Validation and Submission
const forms = {
    houseForm: {
        endpoint: '/predict_house',
        resultId: 'houseResult',
        processResult: (data) => {
            let html = `
                <div class="alert alert-success">
                    <h4>Predicted House Price: ₹${data.prediction.toLocaleString()} lakh</h4>
                    <p>Model Accuracy: ${(data.accuracy * 100).toFixed(2)}%</p>
            `;
            
            if (data.warning) {
                html += `
                    <div class="alert alert-warning mt-2">
                        <i class="fas fa-exclamation-triangle"></i> ${data.warning}
                    </div>
                `;
            }
            
            html += '</div>';
            return html;
        }
    },
    salaryForm: {
        endpoint: '/predict_salary',
        resultId: 'salaryResult',
        processResult: (data) => `
            <div class="alert alert-success">
                <h4>Predicted Salary: ₹${data.prediction.toLocaleString()}</h4>
                <p>Model Accuracy: ${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `
    },
    diabetesForm: {
        endpoint: '/predict_diabetes',
        resultId: 'diabetesResult',
        processResult: (data) => `
            <div class="alert ${data.prediction === 1 ? 'alert-danger' : 'alert-success'}">
                <h4>Diabetes Risk Assessment</h4>
                <p>Prediction: ${data.prediction === 1 ? 'High Risk' : 'Low Risk'}</p>
                <p>Probability: ${data.probability.toFixed(2)}%</p>
                <p>Model Accuracy: ${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `
    },
    fruitForm: {
        endpoint: '/predict_fruit',
        resultId: 'fruitResult',
        processResult: (data) => `
            <div class="alert alert-success">
                <h4>Predicted Fruit: ${data.prediction}</h4>
                <p>Confidence: ${data.confidence.toFixed(2)}%</p>
                <p>Model Accuracy: ${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `
    },
    temperatureForm: {
        endpoint: '/predict_temperature',
        resultId: 'temperatureResult',
        processResult: (data) => `
            <div class="alert alert-info">
                <h4>Predicted Temperature: ${data.prediction.toFixed(1)}°C</h4>
                <p>Model Accuracy: ${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `
    }
};

// Add form submission handlers
document.querySelectorAll('.prediction-form').forEach(formContainer => {
    const form = formContainer.querySelector('form');
    const formId = formContainer.id;
    const config = forms[formId];
    const resultDiv = document.getElementById(config.resultId);

    if (form && resultDiv) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Show loading state
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-spinner fa-spin"></i> Processing...
                </div>
            `;
            
            try {
                // Collect form data
                const formData = new FormData(form);
                const data = {};
                for (const [key, value] of formData.entries()) {
                    data[key] = value;
                }

                // Validate form data
                if (!validateForm(form)) {
                    throw new Error('Please fill in all required fields correctly');
                }
                
                // Send prediction request
                const response = await fetch(config.endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Prediction failed');
                }
                
                const result = await response.json();
                
                // Display result
                resultDiv.innerHTML = config.processResult(result);
                
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <h4>Error</h4>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        });
    }
});

// Form Validation
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else if (input.type === 'number') {
            const value = parseFloat(input.value);
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);

            if (isNaN(value)) {
                showError(input, 'Please enter a valid number');
                isValid = false;
            } else if (min !== undefined && value < min) {
                showError(input, `Value must be at least ${min}`);
                isValid = false;
            } else if (max !== undefined && value > max) {
                showError(input, `Value must be at most ${max}`);
                isValid = false;
            }
        }
    });

    return isValid;
}

// Error Display
function showError(element, message) {
    const formGroup = element.closest('.form-group');
    if (formGroup) {
        const feedback = formGroup.querySelector('.invalid-feedback') || 
                        createErrorFeedback(formGroup);
        
        feedback.textContent = message;
        element.classList.add('is-invalid');
    }
}

function createErrorFeedback(formGroup) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    formGroup.appendChild(feedback);
    return feedback;
}

// Reset form and error states
function resetForm(form) {
    form.reset();
    form.querySelectorAll('.is-invalid').forEach(element => {
        element.classList.remove('is-invalid');
    });
    form.querySelectorAll('.invalid-feedback').forEach(element => {
        element.remove();
    });
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    // Show the first form by default
    const firstForm = document.querySelector('.prediction-form');
    if (firstForm) {
        firstForm.style.display = 'block';
    }
    
    // Set the first tab as active
    const firstTab = document.querySelector('.model-tab');
    if (firstTab) {
        firstTab.classList.add('active');
    }
});
