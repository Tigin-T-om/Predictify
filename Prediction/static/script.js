// Theme Toggle
const themeSwitch = document.getElementById('theme-switch');
const body = document.body;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.classList.toggle('dark-mode', savedTheme === 'dark');
    themeSwitch.checked = savedTheme === 'dark';
}

themeSwitch.addEventListener('change', () => {
    body.classList.toggle('dark-mode');
    localStorage.setItem('theme', body.classList.contains('dark-mode') ? 'dark' : 'light');
});

// Model Selection
const modelTabs = document.querySelectorAll('.model-tab');
const predictionForms = document.querySelectorAll('.prediction-form');

modelTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and forms
        modelTabs.forEach(t => t.classList.remove('active'));
        predictionForms.forEach(f => f.classList.remove('active'));

        // Add active class to clicked tab and corresponding form
        tab.classList.add('active');
        const formId = tab.getAttribute('data-form');
        const targetForm = document.getElementById(formId);
        if (targetForm) {
            targetForm.classList.add('active');
            // Reset forms and results when switching tabs
            resetForms();
            resetResults();
        } else {
            console.error('Form not found:', formId);
        }
    });
});

// Form Validation and Submission
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!validateForm(form)) {
        return;
    }

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Predicting...';

        try {
            const response = await fetch(form.action, {
        method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

        if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            console.log('Prediction result:', result); // Debug log

            // Display results
            displayResults(form.id, result);

        } catch (error) {
            console.error('Error:', error); // Debug log
            showError(form.id, error.message);
        } finally {
            // Reset button state
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
});

// Form Validation
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else if (input.type === 'number') {
            const value = parseFloat(input.value);
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);

            // Special validation for salary prediction
            if (form.id === 'salaryForm') {
                if (input.id === 'education_level' && (value < 1 || value > 3)) {
                    showError(input, 'Education level must be between 1 and 3');
                    isValid = false;
                }
                if (input.id === 'years_experience' && value < 0) {
                    showError(input, 'Years of experience cannot be negative');
                    isValid = false;
                }
                if (input.id === 'certifications' && value < 0) {
                    showError(input, 'Number of certifications cannot be negative');
                    isValid = false;
                }
            }

            // Special validation for house price prediction
            if (form.id === 'houseForm' && input.id === 'sqft') {
                if (value < 100) {
                    showError(input, 'Square footage must be at least 100 sq ft');
                    isValid = false;
                }
            }

            // Special validation for temperature prediction
            if (form.id === 'temperatureForm') {
                if (input.id === 'day' && (value < 1 || value > 31)) {
                    showError(input, 'Day must be between 1 and 31');
                    isValid = false;
                }
                if (input.id === 'humidity' && (value < 0 || value > 100)) {
                    showError(input, 'Humidity must be between 0% and 100%');
                    isValid = false;
                }
                if (input.id === 'wind_speed' && (value < 0 || value > 100)) {
                    showError(input, 'Wind speed must be between 0 and 100 km/h');
                    isValid = false;
                }
                if (input.id === 'pressure' && (value < 900 || value > 1100)) {
                    showError(input, 'Pressure must be between 900 and 1100 hPa');
                    isValid = false;
                }
            }

            // Special validation for fruit classification
            if (form.id === 'fruitForm') {
                if (input.id === 'weight' && value <= 0) {
                    showError(input, 'Weight must be greater than 0');
                    isValid = false;
                }
                if (input.id === 'size' && value <= 0) {
                    showError(input, 'Size must be greater than 0');
                    isValid = false;
                }
                if (input.id === 'color_score' && (value < 0 || value > 1)) {
                    showError(input, 'Color score must be between 0 and 1');
                    isValid = false;
                }
            }

            if (isNaN(value) || (min !== undefined && value < min) || (max !== undefined && value > max)) {
                showError(input, `Please enter a number between ${min} and ${max}`);
                isValid = false;
            }
        }
    });

    return isValid;
}

// Error Display
function showError(element, message) {
    const formGroup = element.closest('.form-group');
    const feedback = formGroup.querySelector('.invalid-feedback') || 
                    createErrorFeedback(formGroup);
    
    feedback.textContent = message;
    element.classList.add('is-invalid');
}

function createErrorFeedback(formGroup) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    formGroup.appendChild(feedback);
    return feedback;
}

// Results Display
function displayResults(formId, result) {
    console.log('Displaying results for form:', formId); // Debug log
    
    // For the fruit form, we need to handle it specially
    if (formId === 'fruitForm') {
        const resultSection = document.getElementById('fruitResult');
        if (!resultSection) {
            console.error('Result section not found for form:', formId);
            return;
        }
        
        const resultContent = resultSection.querySelector('.result-content');
        if (!resultContent) {
            console.error('Result content not found for form:', formId);
            return;
        }
        
        displayFruitResult(resultContent, result);
        resultSection.classList.remove('d-none');
        return;
    }
    
    // Handle other forms
    const resultSection = document.querySelector(`#${formId.replace('Form', 'Result')}`);
    if (!resultSection) {
        console.error('Result section not found for form:', formId); // Debug log
        return;
    }

    const resultContent = resultSection.querySelector('.result-content');
    if (!resultContent) {
        console.error('Result content not found for form:', formId); // Debug log
        return;
    }
    
    // Clear previous results
    resultContent.innerHTML = '';
    
    // Create result elements based on model type
    switch(formId) {
        case 'houseForm':
            displayHouseResult(resultContent, result);
            break;
        case 'salaryForm':
            displaySalaryResult(resultContent, result);
            break;
        case 'diabetesForm':
            displayDiabetesResult(resultContent, result);
            break;
        case 'temperatureForm':
            displayTemperatureResult(resultContent, result);
            break;
        default:
            console.error('Unknown form ID:', formId); // Debug log
    }
    
    // Show result section
    resultSection.classList.remove('d-none');
}

// Model-specific result displays
function displayHouseResult(container, result) {
    // Ensure minimum price of $100,000
    const predictedPrice = Math.max(result.prediction, 100000);
    
    container.innerHTML = `
        <div class="alert alert-success">
            <h4 class="alert-heading">Predicted House Price</h4>
            <p class="mb-0">$${predictedPrice.toLocaleString()}</p>
        </div>
        <div class="alert alert-info">
            <h4 class="alert-heading">Model Accuracy</h4>
            <p class="mb-0">${(result.accuracy * 100).toFixed(2)}%</p>
        </div>
    `;
}

function displaySalaryResult(container, result) {
    container.innerHTML = `
        <div class="alert alert-success">
            <h4 class="alert-heading">Predicted Annual Salary</h4>
            <p class="mb-0">$${result.prediction.toLocaleString(undefined, {maximumFractionDigits: 0})}</p>
        </div>
        <div class="alert alert-info">
            <h4 class="alert-heading">Model Accuracy</h4>
            <p class="mb-0">${(result.accuracy * 100).toFixed(2)}%</p>
        </div>
    `;
}

function displayDiabetesResult(container, result) {
    // Determine alert class based on risk level
    let alertClass = 'alert-info';
    if (result.diabetes_risk === 'High Risk') {
        alertClass = 'alert-danger';
    } else if (result.diabetes_risk === 'Moderate Risk') {
        alertClass = 'alert-warning';
    }
    
    container.innerHTML = `
        <div class="alert ${alertClass}">
            <h4 class="alert-heading">Diabetes Risk Assessment</h4>
            <p class="mb-0">Risk Level: ${result.diabetes_risk}</p>
            <p class="mb-0">Probability: ${result.probability}%</p>
        </div>
        <div class="alert alert-info">
            <h4 class="alert-heading">Model Accuracy</h4>
            <p class="mb-0">${result.model_accuracy}%</p>
        </div>
        <div class="card mt-3">
            <div class="card-body">
                <h5 class="card-title">Input Values</h5>
                <ul class="list-unstyled mb-0">
                    <li>Age: ${result.age} years</li>
                    <li>BMI: ${result.bmi}</li>
                    <li>Glucose Level: ${result.glucose_level} mg/dL</li>
                    <li>Blood Pressure: ${result.blood_pressure} mmHg</li>
                </ul>
            </div>
        </div>
    `;
}

function displayFruitResult(container, result) {
    container.innerHTML = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Fruit Classification Result</h5>
                <div class="alert alert-success">
                    <h4 class="mb-0">Predicted Fruit: ${result.prediction}</h4>
                    <p class="mb-0">Confidence: ${(result.confidence * 100).toFixed(2)}%</p>
                </div>
                <div class="mt-3">
                    <h6>Top Predictions:</h6>
                    <ul class="list-group">
                        ${result.top_predictions.map(pred => `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                ${pred.fruit}
                                <span class="badge bg-primary rounded-pill">${(pred.probability * 100).toFixed(2)}%</span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                <div class="mt-3">
                    <small class="text-muted">Model Accuracy: ${result.model_accuracy}%</small>
                </div>
            </div>
        </div>
    `;
}

function displayTemperatureResult(container, result) {
    container.innerHTML = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Temperature Prediction Result</h5>
                <div class="alert alert-success">
                    <h4 class="mb-0">Predicted Temperature: ${result.prediction.toFixed(1)}°C</h4>
                </div>
                <div class="mt-3">
                    <p>Input Parameters:</p>
                    <ul class="list-group">
                        <li class="list-group-item">Day: ${result.day}</li>
                        <li class="list-group-item">Humidity: ${result.humidity.toFixed(1)}%</li>
                        <li class="list-group-item">Wind Speed: ${result.wind_speed.toFixed(1)} km/h</li>
                        <li class="list-group-item">Pressure: ${result.pressure.toFixed(1)} hPa</li>
                    </ul>
                </div>
                <div class="mt-3">
                    <small class="text-muted">Model Accuracy: ${result.model_accuracy.toFixed(1)}%</small>
                </div>
            </div>
        </div>
    `;
}

// Reset Functions
function resetForms() {
    forms.forEach(form => {
        form.reset();
        const inputs = form.querySelectorAll('.is-invalid');
        inputs.forEach(input => {
            input.classList.remove('is-invalid');
        });
    });
}

function resetResults() {
    document.querySelectorAll('.result-section').forEach(section => {
        section.classList.add('d-none');
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set initial active tab and form
    const firstTab = modelTabs[0];
    firstTab.classList.add('active');
    const firstForm = document.getElementById(firstTab.getAttribute('data-form'));
    if (firstForm) {
        firstForm.classList.add('active');
    } else {
        console.error('Initial form not found');
    }
});
