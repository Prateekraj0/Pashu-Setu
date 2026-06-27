async function analyzeImage(type) {
    try {
        let file;

        if (type === "breed") {
            file = document.querySelector('#dz-breed input').files[0];
        } else {
            file = document.querySelector('#dz-disease input').files[0];
        }

        if (!file) {
            alert("Upload image first");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://127.0.0.1:5001/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const text = await response.text();
            console.error(text);
            alert("Backend error");
            return;
        }

        const data = await response.json();

        // =========================
        // BREED RESULT
        // =========================
        document.getElementById("rp-breed").innerHTML = `
            <h3>Breed: ${data.breed}</h3>
            <p>Confidence: ${(data.breed_conf * 100).toFixed(2)}%</p>
        `;

        // =========================
        // DISEASE RESULT
        // =========================
        document.getElementById("rp-disease").innerHTML = `
            <h3>Disease: ${data.disease}</h3>
            <p>Confidence: ${(data.disease_conf * 100).toFixed(2)}%</p>
        `;

        // =========================
        // BREED INFO
        // =========================
        if (data.breed_info && data.breed_info.length > 0) {
            const info = data.breed_info[0];

            document.getElementById("rp-breed").innerHTML += `
                <p><b>Origin:</b> ${info["Region of Origin (India/World)"] || "N/A"}</p>
                <p><b>Milk Yield:</b> ${info["Avg. Milk Yield (L/day)"] || "N/A"}</p>
                <p><b>Milk Type:</b> ${info["Milk Type (Fat %)"] || "N/A"}</p>
                <p><b>Utility:</b> ${info["Utility"] || "N/A"}</p>
            `;
        }

    } catch (error) {
        console.error(error);
        alert("❌ Cannot connect to backend");
    }
}