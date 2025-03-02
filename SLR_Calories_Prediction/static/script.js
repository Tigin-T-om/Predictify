function predictCalories() {
    let steps = document.getElementById("steps").value.trim();

    // Validate input
    if (!steps || isNaN(steps) || steps <= 0) {
        alert("Please enter a valid number of steps.");
        return;
    }

    // Show loading message
    document.getElementById("result").innerHTML = "Calculating...";

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ steps: parseFloat(steps) })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server response was not OK");
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("result").innerHTML = 
            `Predicted Calories Burned: ${data.calories_burned.toFixed(2)}`;
        
        console.log("Received Accuracy:", data.accuracy);  // Debugging

        // Ensure accuracy is updated dynamically
        if (data.accuracy) {
            document.getElementById("accuracy").innerText = data.accuracy;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = "Error in prediction. Try again.";
    });
}
