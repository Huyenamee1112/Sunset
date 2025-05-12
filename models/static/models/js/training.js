document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#training-form");

    const trainButton = document.getElementById("trainButton");
    const loader = document.getElementById("trainLoader");
    const timeDisplay = document.getElementById("train_timeDisplay");

    const trainText = document.getElementById("trainText");

    let timerInterval;
    let secondsElapsed = 0;

    function startTimer() {
        secondsElapsed = 0;
        trainText.classList.add("d-none");
        timeDisplay.classList.remove("d-none");
        timerInterval = setInterval(() => {
            secondsElapsed++;
            timeDisplay.textContent = `${secondsElapsed}s`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
        timeDisplay.classList.add("d-none");
        trainText.classList.remove("d-none");
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const dataset = document.getElementById("train_dataset").value;
        const model = document.getElementById("train_model").value;
        const modelName = document.getElementById("model_name").value.trim();

        // Xóa các thông báo lỗi cũ
        const errorMessages = document.querySelectorAll(".error-message");
        errorMessages.forEach(msg => msg.remove());

        let valid = true;

        if (!dataset) {
            valid = false;
            showError("dataset", "Please select a dataset.");
        }

        if (!model) {
            valid = false;
            showError("model", "Please select a model.");
        }

        if (!modelName) {
            valid = false;
            showError("model_name", "Model name is required.");
        } else if (!/^[a-zA-Z0-9_-]+$/.test(modelName)) {
            valid = false;
            showError("model_name", "Model name cannot contain special characters or spaces.");
        }

        if (!valid) return;

        loader.classList.remove("d-none");
        trainButton.disabled = true;
        startTimer();

        try {
            const trainingUrl = "/api/training/";

            const response = await fetch(trainingUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    dataset: dataset,
                    model: model,
                    model_name: modelName,
                }),
            });

            const result = await response.json();

            loader.classList.add("d-none");
            trainButton.disabled = false;
            stopTimer();

            if (response.ok) {
                alert(result.message);
            } else {
                alert(result.error || "Something went wrong");
            }
        } catch (err) {
            loader.classList.add("d-none");
            trainButton.disabled = false;
            stopTimer();
            alert("JS Error: " + err.message);
        }
    });

    function showError(inputId, message) {
        const inputElement = document.getElementById(inputId);
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("error-message", "text-danger");
        errorMessage.textContent = message;
        inputElement.parentElement.appendChild(errorMessage);
    }
});
