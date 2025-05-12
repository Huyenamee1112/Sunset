document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#testing-form");

    const testButton = document.getElementById("testButton");
    const loader = document.getElementById("testLoader");
    const timeDisplay = document.getElementById("test_timeDisplay");
    const testText = document.getElementById("testText");
    const testResultSection = document.getElementById("testResult");
    const resultTable = document.getElementById("resultTable");
    const confusionMatrixRow = document.getElementById("confMatrixRow");

    let timerInterval;
    let secondsElapsed = 0;

    function startTimer() {
        clearInterval(timerInterval);  // Đảm bảo không chạy song song
        secondsElapsed = 0;
        timeDisplay.textContent = "0s";
        testText.classList.add("d-none");
        timeDisplay.classList.remove("d-none");
        timerInterval = setInterval(() => {
            secondsElapsed++;
            timeDisplay.textContent = `${secondsElapsed}s`;
        }, 1000);
    }

    function stopTimer() {
        clearInterval(timerInterval);
        timeDisplay.classList.add("d-none");
        testText.classList.remove("d-none");
    }

    function showError(inputId, message) {
        const inputElement = document.getElementById(inputId);
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("error-message", "text-danger");
        errorMessage.textContent = message;
        inputElement.parentElement.appendChild(errorMessage);
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const dataset = document.getElementById("test_dataset").value;
        const model = document.getElementById("test_model").value;

        // Xóa các thông báo lỗi cũ
        document.querySelectorAll(".error-message").forEach(msg => msg.remove());

        let valid = true;
        if (!dataset) {
            valid = false;
            showError("test_dataset", "Please select a dataset.");
        }
        if (!model) {
            valid = false;
            showError("test_model", "Please select a model.");
        }
        if (!valid) return;

        // Reset kết quả trước khi gửi
        testResultSection.classList.add("d-none");
        resultTable.innerHTML = "";
        if (confusionMatrixRow) confusionMatrixRow.innerHTML = "";

        loader.classList.remove("d-none");
        testButton.disabled = true;
        startTimer();

        try {
            const response = await fetch("/api/testing/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ dataset, model }),
            });

            const result = await response.json();

            loader.classList.add("d-none");
            testButton.disabled = false;
            stopTimer();

            if (response.ok) {
                testResultSection.classList.remove("d-none");

                // Hiển thị kết quả
                for (const [metric, value] of Object.entries(result.result)) {
                    const row = document.createElement("tr");
                    if (metric === "f1_score") {
                        row.innerHTML = `<td>${metric}</td><td>Macro: ${value.macro}, Weighted: ${value.weighted}</td>`;
                    } else if (["accuracy", "precision", "recall"].includes(metric)) {
                        row.innerHTML = `<td>${metric}</td><td>${value}</td>`;
                    }
                    resultTable.appendChild(row);
                }

                // Confusion matrix
                if (result.result.confusion_matrix && confusionMatrixRow) {
                    const cm = result.result.confusion_matrix;
                    confusionMatrixRow.innerHTML = `
                        <td>${cm[0][0]}</td>
                        <td>${cm[0][1]}</td>
                        <td>${cm[1][0]}</td>
                        <td>${cm[1][1]}</td>
                    `;
                }
            } else {
                alert(result.error || "Something went wrong.");
            }
        } catch (err) {
            loader.classList.add("d-none");
            testButton.disabled = false;
            stopTimer();
            alert("JS Error: " + err.message);
        }
    });
});
