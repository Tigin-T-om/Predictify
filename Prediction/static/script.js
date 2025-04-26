// Wait for DOM to be fully loaded before attaching event handlers
document.addEventListener('DOMContentLoaded', function() {
    // Get model info when page loads
    fetch('/get_model_info')
        .then(response => response.json())
        .then(data => {
            console.log('Model info loaded:', data);
        })
        .catch(error => {
            console.error('Error fetching model info:', error);
        });

    // House Price Prediction Form
    const housePriceForm = document.getElementById('house-price-form');
    if (housePriceForm) {
        housePriceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(housePriceForm);
            const resultDiv = document.getElementById('house-price-result');
            
            // Show loading state
            resultDiv.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div> Processing...';
            resultDiv.style.display = 'block';
            
            fetch('/predict_house_price', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Modified to include "lakhs" in the output
                    resultDiv.innerHTML = `<h4>Predicted House Price:</h4><p class="fs-3 fw-bold">${data.prediction} lakhs</p>`;
                    resultDiv.className = 'mt-4 result-success';
                } else {
                    resultDiv.innerHTML = `<h4>Error:</h4><p>${data.error}</p>`;
                    resultDiv.className = 'mt-4 result-error';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<h4>Error:</h4><p>An unexpected error occurred: ${error.message}</p>`;
                resultDiv.className = 'mt-4 result-error';
            });
        });
    }

    // Employee Salary Prediction Form
    const salaryForm = document.getElementById('salary-form');
    if (salaryForm) {
        salaryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(salaryForm);
            const resultDiv = document.getElementById('salary-result');
            
            // Show loading state
            resultDiv.innerHTML = '<div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading...</span></div> Processing...';
            resultDiv.style.display = 'block';
            
            fetch('/predict_salary', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `<h4>Predicted Annual Salary:</h4><p class="fs-3 fw-bold">${data.prediction}</p>`;
                    resultDiv.className = 'mt-4 result-success';
                } else {
                    resultDiv.innerHTML = `<h4>Error:</h4><p>${data.error}</p>`;
                    resultDiv.className = 'mt-4 result-error';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<h4>Error:</h4><p>An unexpected error occurred: ${error.message}</p>`;
                resultDiv.className = 'mt-4 result-error';
            });
        });
    }

    // Temperature Prediction Form
    const temperatureForm = document.getElementById('temperature-form');
    if (temperatureForm) {
        temperatureForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(temperatureForm);
            const resultDiv = document.getElementById('temperature-result');
            
            // Make sure precipitation_type is included
            if (!formData.has('precipitation_type')) {
                // Default to 'None' if not selected
                formData.append('precipitation_type', 'None');
            }
            
            // Show loading state
            resultDiv.innerHTML = '<div class="spinner-border text-info" role="status"><span class="visually-hidden">Loading...</span></div> Processing...';
            resultDiv.style.display = 'block';
            
            fetch('/predict_temperature', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `<h4>Predicted Temperature:</h4><p class="fs-3 fw-bold">${data.prediction}°C</p>`;
                    resultDiv.className = 'mt-4 result-success';
                } else {
                    resultDiv.innerHTML = `<h4>Error:</h4><p>${data.error}</p>`;
                    resultDiv.className = 'mt-4 result-error';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<h4>Error:</h4><p>An unexpected error occurred: ${error.message}</p>`;
                resultDiv.className = 'mt-4 result-error';
            });
        });
    }

    // Fruit Classification Form
    const fruitForm = document.getElementById('fruit-form');
    if (fruitForm) {
        fruitForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(fruitForm);
            const resultDiv = document.getElementById('fruit-result');
            
            // Show loading state
            resultDiv.innerHTML = '<div class="spinner-border text-warning" role="status"><span class="visually-hidden">Loading...</span></div> Processing...';
            resultDiv.style.display = 'block';
            
            fetch('/predict_fruit', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `<h4>Classified Fruit:</h4><p class="fs-3 fw-bold">${data.prediction}</p>`;
                    resultDiv.className = 'mt-4 result-success';
                } else {
                    resultDiv.innerHTML = `<h4>Error:</h4><p>${data.error}</p>`;
                    resultDiv.className = 'mt-4 result-error';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<h4>Error:</h4><p>An unexpected error occurred: ${error.message}</p>`;
                resultDiv.className = 'mt-4 result-error';
            });
        });
    }

    // Diabetes Prediction Form
    const diabetesForm = document.getElementById('diabetes-form');
    if (diabetesForm) {
        diabetesForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(diabetesForm);
            const resultDiv = document.getElementById('diabetes-result');
            
            // Show loading state
            resultDiv.innerHTML = '<div class="spinner-border text-danger" role="status"><span class="visually-hidden">Loading...</span></div> Processing...';
            resultDiv.style.display = 'block';
            
            fetch('/predict_diabetes', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resultDiv.innerHTML = `
                        <h4>Diabetes Prediction:</h4>
                        <p class="fs-3 fw-bold">${data.prediction}</p>
                        <p class="fs-5">Probability: ${data.probability}</p>
                        <div class="alert alert-warning mt-3">
                            <strong>Disclaimer:</strong> This is a demonstration model only and should not be used for actual medical diagnosis.
                            Always consult a healthcare professional for medical advice.
                        </div>
                    `;
                    resultDiv.className = 'mt-4 result-success';
                } else {
                    resultDiv.innerHTML = `<h4>Error:</h4><p>${data.error}</p>`;
                    resultDiv.className = 'mt-4 result-error';
                }
            })
            .catch(error => {
                resultDiv.innerHTML = `<h4>Error:</h4><p>An unexpected error occurred: ${error.message}</p>`;
                resultDiv.className = 'mt-4 result-error';
            });
        });
    }

    // Initialize proper tab handling for form IDs with same names across tabs
    const tabLinks = document.querySelectorAll('.nav-link');
    if (tabLinks) {
        tabLinks.forEach(tabLink => {
            tabLink.addEventListener('click', function() {
                // Clear all previous results when switching tabs
                const resultDivs = document.querySelectorAll('[id$="-result"]');
                resultDivs.forEach(div => {
                    div.style.display = 'none';
                    div.innerHTML = '';
                });
            });
        });
    }

    // Set default values for forms to make testing easier
    // House Price Form
    if (document.getElementById('square_footage')) {
        document.getElementById('square_footage').value = '1500';
    }

    // Salary Form
    if (document.getElementById('age')) {
        document.getElementById('age').value = '35';
        document.getElementById('experience').value = '10';
    }

    // Temperature Form
    if (document.getElementById('apparent_temperature')) {
        document.getElementById('apparent_temperature').value = '25.5';
        document.getElementById('humidity').value = '0.7';
        document.getElementById('wind_speed').value = '10.2';
        document.getElementById('wind_bearing').value = '180';
        document.getElementById('visibility').value = '15.0';
        document.getElementById('cloud_cover').value = '0.3';
        document.getElementById('pressure').value = '1012.5';
        document.getElementById('year').value = '2025';
        document.getElementById('month').value = '4';
        document.getElementById('day').value = '15';
        document.getElementById('hour').value = '14';
        
        // Set default for precipitation type
        const precipitationTypeRadios = document.querySelectorAll('input[name="precipitation_type"]');
        if (precipitationTypeRadios.length > 0) {
            precipitationTypeRadios[0].checked = true; // Select "None" by default
        }
    }

    // Fruit Form
    if (document.getElementById('mass')) {
        document.getElementById('mass').value = '150';
        document.getElementById('width').value = '7.5';
        document.getElementById('height').value = '9.2';
        document.getElementById('color_score').value = '0.75';
    }

    // Diabetes Form
    if (document.getElementById('age-diabetes')) {
        document.getElementById('age-diabetes').value = '45';
        document.getElementById('bmi').value = '26.5';
        document.getElementById('hba1c').value = '5.7';
        document.getElementById('glucose').value = '120';
    }
});