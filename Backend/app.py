from flask import Flask, request, jsonify
from flask_cors import CORS
import onnxruntime as ort
import numpy as np
import pandas as pd
from PIL import Image
import io
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

# ============================
# LOAD MODELS
# ============================

disease_session = ort.InferenceSession("model.onnx")
breed_model = YOLO("bovine_best.pt")

df = pd.read_excel("breeds.xlsx")

disease_classes = [
    "Foot-and-Mouth Disease",
    "Healthy",
    "Lumpy Skin Disease"
]

# Debug (prints when server starts)
print("Disease model input shape:", disease_session.get_inputs()[0].shape)

# ============================
# IMAGE PREPROCESS
# ============================

def preprocess_image(file):

    image = Image.open(io.BytesIO(file)).convert("RGB")
    image = image.resize((224, 224))

    img = np.array(image).astype(np.float32)

    # normalize
    img = img / 255.0

    # TensorFlow format → (1,224,224,3)
    img = np.expand_dims(img, axis=0)

    return img


# ============================
# ROUTES
# ============================

@app.route("/")
def home():
    return "Backend is running ✅"


@app.route("/predict", methods=["POST"])
def predict():
    try:

        file = request.files["file"].read()

        # =========================
        # DISEASE PREDICTION
        # =========================

        img = preprocess_image(file)

        input_name = disease_session.get_inputs()[0].name

        disease_pred = disease_session.run(
            None,
            {input_name: img}
        )[0]

        disease_idx = int(np.argmax(disease_pred))
        disease_conf = float(np.max(disease_pred))
        disease_name = disease_classes[disease_idx]

        # =========================
        # BREED PREDICTION
        # =========================

        image = Image.open(io.BytesIO(file))

        results = breed_model(image)

        if results[0].probs is not None:

            probs = results[0].probs

            breed_idx = int(probs.top1)
            breed_conf = float(probs.top1conf)

            breed_name = results[0].names[breed_idx]

        else:

            breed_name = "Unknown"
            breed_conf = 0.0

        # =========================
        # BREED INFO
        # =========================

        breed_info = []

        if "Breed Name" in df.columns:

            breed_info = df[
                df["Breed Name"]
                .str.lower()
                .str.contains(breed_name.lower(), na=False)
            ].to_dict(orient="records")

        # =========================
        # RESPONSE
        # =========================

        return jsonify({
            "disease": disease_name,
            "disease_conf": disease_conf,
            "breed": breed_name,
            "breed_conf": breed_conf,
            "breed_info": breed_info
        })

    except Exception as e:

        print("🔥 ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


# ============================
# RUN SERVER
# ============================

if __name__ == "__main__":
    app.run(debug=True, port=5001)
