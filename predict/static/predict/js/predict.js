document.getElementById("predict-form").addEventListener("submit", function(e) {
    e.preventDefault();

    // Clear previous results
    document.getElementById("download_pred").classList.add("d-none");
    document.getElementById("download_prob").classList.add("d-none");

    const valDiv = document.getElementById("validationMetrics");
    valDiv.innerHTML = "";
    document.getElementById("validationResult").classList.add("d-none");
    document.getElementById("predictResult").classList.add("d-none");

    const form = e.target;
    const formData = new FormData(form);
    const button = document.getElementById("predictButton");
    const loader = document.getElementById("predictLoader");
    const text = document.getElementById("predictText");

    button.disabled = true;
    loader.classList.remove("d-none");
    text.textContent = "Predicting...";

    fetch("/api/predict/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.error || "Unknown error occurred.");
            });
        }
        return response.json();
    })
    .then(data => {
        // Hiển thị file tải xuống - y_pred
        if (data.y_pred) {
            const blobPred = new Blob([data.y_pred.join("\n")], { type: "text/plain" });
            const downloadPred = document.getElementById("download_pred");
            downloadPred.href = URL.createObjectURL(blobPred);
            downloadPred.classList.remove("d-none");
        }

        // Hiển thị file tải xuống - y_pred_prob
        if (data.y_pred_prob) {
            const blobProb = new Blob([data.y_pred_prob.join("\n")], { type: "text/plain" });
            const downloadProb = document.getElementById("download_prob");
            downloadProb.href = URL.createObjectURL(blobProb);
            downloadProb.classList.remove("d-none");
        }

        // Hiển thị các chỉ số đánh giá
        if (data.validation_metrics) {
            const valDiv = document.getElementById("validationMetrics");
            valDiv.innerHTML = "";
            for (const [metric, value] of Object.entries(data.validation_metrics)) {
                valDiv.innerHTML += `<p><strong>${metric}</strong>: ${value}</p>`;
            }
            document.getElementById("validationResult").classList.remove("d-none");
        }

        document.getElementById("predictResult").classList.remove("d-none");
    })
    .catch(err => {
        alert(`Prediction failed: ${err.message}`);
    })
    .finally(() => {
        button.disabled = false;
        loader.classList.add("d-none");
        text.textContent = "Predict";
    });
});
