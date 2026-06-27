# 🚀 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Indian-Bovine-Recognition-System.git
cd Indian-Bovine-Recognition-System
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Download the Trained Model

The trained YOLOv8 model is not included in this repository due to GitHub file size limitations.

Download it from the link below:

🔗 **Model Download**

https://drive.google.com/file/d/1T31KMKoPpxXPbjQtYxIk14f_UoFbFstL/view?usp=sharing

After downloading, place the model inside:

```text
backend/
│
├── bovine_best.pt
```

---

## 4️⃣ Extract Breed Information

The breed information file (`breeds.xlsx`) is provided inside a ZIP archive.

Extract the ZIP file and place **breeds.xlsx** inside the backend folder:

```text
backend/
│
├── breeds.xlsx
```

---

## 5️⃣ Run the Backend

```bash
python backend/app.py
```

---

## 6️⃣ Launch the Frontend

Open

```text
frontend/index.html
```

in your preferred browser.

---

# 📂 Final Project Structure

```text
Indian-Bovine-Recognition-System
│
├── backend
│   ├── app.py
│   ├── bovine_best.pt          ← Download separately
│   ├── breeds.xlsx             ← Extract from ZIP
│   └── model.onnx
│
├── frontend
│   ├── index.html
│   └── script.js
│
├── requirements.txt
└── README.md
```

---

# ⚠️ Important Notes

- The trained model is hosted on Google Drive because it exceeds GitHub's file size limit.
- Before running the application, ensure **bovine_best.pt** is placed inside the **backend** folder.
- Extract the ZIP archive containing **breeds.xlsx** and place the Excel file inside the **backend** folder.
- Verify that all required dependencies are installed using **requirements.txt**.
