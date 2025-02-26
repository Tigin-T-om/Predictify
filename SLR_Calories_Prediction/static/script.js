function predictCalories() {
    let steps = document.getElementById("steps").value;

    if (!steps) {
        alert("Please enter the number of steps.");
        return;
    }

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ steps: parseFloat(steps) })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = 
            "Predicted Calories Burned: " + data.calories_burned.toFixed(2);
    })
    .catch(error => console.error('Error:', error));
}
