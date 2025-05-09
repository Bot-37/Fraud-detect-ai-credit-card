
# 💳 Credit Card Fraud Detection System with Web Portal

![Fraud Detection Demo](data/Fraud-Detection-Demo.gif) <!-- Replace with actual screenshot path -->

An end-to-end AI-powered system for detecting credit card frauds with a web interface. Combines Machine Learning, Flask backend, and React frontend for real-time fraud tracking and user interaction.

---

## 🔒 Features

- 🛡️ **Real-time Fraud Detection** – Predicts fraud likelihood using a trained ML model.
- 🔍 **Anomaly Detection** – Detects unusual patterns in user behavior and transaction flow.
- 🚨 **Stolen Card Reporting** – Users can report lost/stolen cards via web portal.
- 📊 **Admin Dashboard** – Live transaction feeds, suspicious activity alerts, and metrics.
- 📈 **Behavioral Pattern Analysis** – Tracks individual transaction trends for anomaly risk scoring.
- 🔗 **RESTful API** – Clean, scalable JSON-based API endpoints for integration.

---

## 🧰 Tech Stack

| Layer         | Technology Used                  |
|--------------|----------------------------------|
| Backend       | Flask, Python 3.10+              |
| Machine Learning | Scikit-Learn, Pandas, NumPy      |
| Model Serialization | Joblib                          |
| Frontend      | React, Bootstrap 5               |
| Data Storage  | Local CSV, JSON (Demo)           |

---

## 📦 Project Structure

```
fraud-detect-ai/
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       └── transactions.py
│   ├── app/
│   │   ├── fraud_detector.py
│   │   ├── trainer.py
│   │   ├── utils.py
│   │   └── logs/
│   └── server.py
├── config.py
├── data/
│   ├── creditcard.csv
│   ├── fake_credit_card_dataset.json
│   └── stolen_cards.json
├── frontend/
│   ├── app.jsx
│   ├── main.jsx
│   └── ...
└── fraud_model.pkl
```

---

## 🚀 Installation & Run

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fraud-detect-ai.git
cd fraud-detect-ai
```

### 2. Set Up Python Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

### 3. Set Up React Frontend
```bash
cd frontend
npm install
npm run dev
```

Access the app at `http://localhost:3000`.

---

## 📂 Datasets

- **creditcard.csv** – Based on anonymized European transactions dataset
- **fake_credit_card_dataset.json** – Synthetic data for testing
- **stolen_cards.json** – Simulated stolen card database

---

## 🧠 Model Training (Optional)

If you want to retrain:
```bash
cd backend/app
python trainer.py
```
Model saved as `fraud_model.pkl`.

---

## 🔐 API Endpoints

| Endpoint                   | Method | Description                  |
|---------------------------|--------|------------------------------|
| `/api/predict`            | POST   | Predict fraud from data      |
| `/api/report-stolen`      | POST   | Mark card as stolen          |
| `/api/get-transactions`   | GET    | Retrieve transaction logs    |

---

## 📷 Demo

![Fraud Detection Demo](data/Fraud-Detection-Demo.gif)  
_Replace the above path with your real screenshot or GIF demo._

---

## 🛡️ Security Tip

For deployment:
- Use HTTPS
- Add user authentication with token-based access
- Use database instead of JSON for production
- Log all suspicious activity and implement alert triggers

---

## 📜 License

MIT License – Use it responsibly and ethically.

---

## 👨‍💻 Developed by

**Fahad (Boss)**  
Credit Card Fraud Defense Initiative – AI + Security Lab  
