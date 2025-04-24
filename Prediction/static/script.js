/**
 * ML Prediction Dashboard JavaScript
 * Handles form submissions, tab switching, and theme toggling
 */

document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeSwitch = document.getElementById('theme-switch');
    const body = document.body;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeSwitch.checked = true;
    }
    
    // Theme switch event listener
    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Model tab switching
    const modelTabs = document.querySelectorAll('.model-tab');
    const predictionForms = document.querySelectorAll('.prediction-form');
    
    modelTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs and forms
            modelTabs.forEach(t => t.classList.remove('active'));
            predictionForms.forEach(form => form.classList.remove('active'));
            
            // Add active class to selected tab
            this.classList.add('active');
            
            // Show the corresponding form
            const formId = this.getAttribute('data-form');
            document.getElementById(formId).classList.add('active');
        });
    });
    
    // House Price Prediction Form
    const housePredictionForm = document.getElementById('housePredictionForm');
    const houseResult = document.getElementById('houseResult');
    
    housePredictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        houseResult.innerHTML = '<div class="alert alert-info">Processing your request... <span class="loading"></span></div>';
        houseResult.style.display = 'block';
        
        // Get form data
        const formData = new FormData(this);
        const squareFootage = formData.get('square_footage');
        
        // Send API request
        fetch('/predict/house', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                square_footage: squareFootage
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                houseResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                const price = parseFloat(data.predicted_price).toLocaleString('en-US', {
                    style: 'currency',
                    currency: 'USD'
                });
                
                houseResult.innerHTML = `
                    <div class="alert alert-success">
                        <h4>Prediction Result</h4>
                        <p>Based on ${squareFootage} square feet:</p>
                        <div class="prediction-value">${price}</div>
                    </div>
                `;
            }
        })
        .catch(error => {
            houseResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
        });
    });
    
    // Salary Prediction Form
    const salaryPredictionForm = document.getElementById('salaryPredictionForm');
    const salaryResult = document.getElementById('salaryResult');
    
    salaryPredictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        salaryResult.innerHTML = '<div class="alert alert-info">Processing your request... <span class="loading"></span></div>';
        salaryResult.style.display = 'block';
        
        // Get form data
        const formData = new FormData(this);
        
        // Send API request
        fetch('/predict/salary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                age: formData.get('age'),
                years_experience: formData.get('years_experience'),
                gender: formData.get('gender'),
                education_level: formData.get('education_level'),
                job_title: formData.get('job_title')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                salaryResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                const salary = parseFloat(data.predicted_salary).toLocaleString('en-US', {
                    style: 'currency',
                    currency: 'USD'
                });
                
                salaryResult.innerHTML = `
                    <div class="alert alert-success">
                        <h4>Prediction Result</h4>
                        <p>For a ${formData.get('gender')} ${formData.get('age')} years old with ${formData.get('years_experience')} years of experience, 
                        ${formData.get('education_level')} education, working as ${formData.get('job_title')}:</p>
                        <div class="prediction-value">${salary} annual salary</div>
                    </div>
                `;
            }
        })
        .catch(error => {
            salaryResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
        });
    });
    
    // Diabetes Risk Prediction Form
    const diabetesPredictionForm = document.getElementById('diabetesPredictionForm');
    const diabetesResult = document.getElementById('diabetesResult');
    
    diabetesPredictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        diabetesResult.innerHTML = '<div class="alert alert-info">Processing your request... <span class="loading"></span></div>';
        diabetesResult.style.display = 'block';
        
        // Get form data
        const formData = new FormData(this);
        
        // Send API request
        fetch('/predict/diabetes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gender: formData.get('gender'),
                age: formData.get('age'),
                hypertension: formData.get('hypertension'),
                heart_disease: formData.get('heart_disease'),
                smoking_history: formData.get('smoking_history'),
                bmi: formData.get('bmi'),
                hba1c_level: formData.get('hba1c_level'),
                blood_glucose_level: formData.get('blood_glucose_level')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                diabetesResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                const riskClass = data.risk_level === 'High' ? 'alert-danger' : 
                                 (data.risk_level === 'Medium' ? 'alert-warning' : 'alert-success');
                
                diabetesResult.innerHTML = `
                    <div class="alert ${riskClass}">
                        <h4>Prediction Result</h4>
                        <p>Based on your health information:</p>
                        <div class="prediction-value">
                            ${data.has_diabetes ? 'Positive' : 'Negative'} for Diabetes
                        </div>
                        <p>Risk Level: <strong>${data.risk_level}</strong></p>
                        <p>${data.recommendation}</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            diabetesResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
        });
    });
    
    // Fruit Classification Form
    const fruitPredictionForm = document.getElementById('fruitPredictionForm');
    const fruitResult = document.getElementById('fruitResult');
    
    fruitPredictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        fruitResult.innerHTML = '<div class="alert alert-info">Processing your request... <span class="loading"></span></div>';
        fruitResult.style.display = 'block';
        
        // Get form data
        const formData = new FormData(this);
        
        // Send API request
        fetch('/predict/fruit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mass: formData.get('mass'),
                width: formData.get('width'),
                height: formData.get('height'),
                color_score: formData.get('color_score')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                fruitResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                const confidencePercent = (data.confidence * 100).toFixed(2);
                
                fruitResult.innerHTML = `
                    <div class="alert alert-success">
                        <h4>Classification Result</h4>
                        <p>Based on the measurements:</p>
                        <div class="prediction-value">${data.fruit_type}</div>
                        <p>Confidence: <strong>${confidencePercent}%</strong></p>
                    </div>
                `;
            }
        })
        .catch(error => {
            fruitResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
        });
    });
    
    // Temperature Prediction Form
    const temperaturePredictionForm = document.getElementById('temperaturePredictionForm');
    const temperatureResult = document.getElementById('temperatureResult');
    
    temperaturePredictionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        temperatureResult.innerHTML = '<div class="alert alert-info">Processing your request... <span class="loading"></span></div>';
        temperatureResult.style.display = 'block';
        
        // Get form data
        const formData = new FormData(this);
        
        // Send API request
        fetch('/predict/temperature', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                day: formData.get('day'),
                humidity: formData.get('humidity'),
                wind_speed: formData.get('wind_speed'),
                pressure: formData.get('pressure')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                temperatureResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                temperatureResult.innerHTML = `
                    <div class="alert alert-success">
                        <h4>Prediction Result</h4>
                        <p>Based on weather conditions:</p>
                        <div class="prediction-value">${data.predicted_temperature}°C</div>
                    </div>
                `;
            }
        })
        .catch(error => {
            temperatureResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
});