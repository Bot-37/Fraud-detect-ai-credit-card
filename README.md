# 💳 Credit Card Fraud Detection System

![Fraud Detection Demo](assets/fraud-detection-demo.gif)

An end-to-end AI-powered solution for detecting credit card frauds in real-time with an intuitive web interface. Powered by Machine Learning, Flask, and React.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![CI/CD Status](https://img.shields.io/github/workflow/status/yourusername/fraud-detect-ai/CI?logo=github)](https://github.com/Bot-37/Fraud-detect-ai-credit-card/actions)

## 📑 Table of Contents

1. [📘 Synopsis](#-synopsis)  
2. [🔒 Key Features](#-key-features)  
3. [🧰 Tech Stack](#-tech-stack)  
4. [📁 Project Structure](#-project-structure)  
5. [🚀 Getting Started](#-getting-started)  
   - [🐍 Backend Setup (Python + Flask)](#-backend-setup-python--flask)  
   - [⚛️ Frontend Setup (React)](#️-frontend-setup-react)  
6. [📂 Datasets](#-datasets)  
7. [🧠 Model Training (Optional)](#-model-training-optional)  
8. [🔐 API Endpoints](#-api-endpoints)  
9. [📈 Performance Metrics](#-performance-metrics)  
10. [🛡️ Security Guidelines for Deployment](#️-security-guidelines-for-deployment)  
11. [👨‍💻 Contributing](#-contributing)  
12. [📜 License](#-license)  
13. [📱 Live Demo Deployment](#-live-demo-deployment)  
    - [🚀 Heroku Deployment](#heroku-deployment)  
    - [🐳 Docker Deployment](#docker-deployment)  
14. [👨‍💻 Developed by](#-developed-by)

## 📘 Synopsis

The **Credit Card Fraud Detection System** is a full-stack, AI-powered web application designed to identify and prevent fraudulent credit card transactions in real-time. Leveraging machine learning models trained on real-world datasets, the platform offers both end-users and administrators intuitive tools to detect, report, and analyze suspicious activity.

Built with **Python (Flask)** on the backend and **React** on the frontend, the system uses a trained ML model to predict fraud, serves RESTful APIs for seamless integration, and presents real-time insights through a responsive web UI. The application also includes security-focused features such as stolen card flagging, behavioral analysis, and a live analytics dashboard.

Whether you're demonstrating fraud detection for a portfolio, testing models, or looking to extend it into production-grade infrastructure, this project provides a solid, extensible foundation.

## 🔒 Key Features

- 🛡️ **Real-time Fraud Prediction** – Predicts the likelihood of fraudulent transactions instantly
- 🔍 **Anomaly Detection** – Spots unusual spending patterns outside of user behavior
- 🚨 **Stolen Card Reporting** – Users can flag lost/stolen cards to prevent unauthorized use
- 📊 **Admin Dashboard** – Live feeds, alerts, and transaction analytics for security teams
- 📈 **Behavioral Analysis** – Detects high-risk deviations from established user behavior
- 🔗 **RESTful APIs** – Clean, scalable, JSON-powered endpoints for integration with existing systems

## 🧰 Tech Stack

| Layer         | Technology             |
|---------------|------------------------|
| Backend       | Flask, Python 3.10+    |
| ML Model      | Scikit-Learn, Pandas, NumPy |
| Serialization | Joblib                 |
| Frontend      | React, Bootstrap 5     |
| Data Storage  | CSV, JSON (Demo)       |

## 📁 Project Structure

```
fraud-detect-ai-credit-card/
├── .github/workflows/       # CI/CD Workflows
├── backend/
│   ├── app/
│   │   ├── api/routes/      # API route logic
│   │   ├── core/            # Configuration
│   │   ├── models/          # Trained model
│   │   ├── main.py          # App entry point
│   │   ├── fraud_detector.py # ML logic
│   │   └── utils.py         # Helper functions
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── styles.css
│   ├── package.json
│   └── tsconfig.json
├── node_modules/
├── .gitignore
├── README.md
├── config.py
└── package-lock.json
```

## 🚀 Getting Started

### 🐍 Backend Setup (Python + Flask)

```bash
# Clone the repository
git clone https://github.com/Bot-37/Fraud-detect-ai-credit-card.git
cd Fraud-detect-ai-credit-card/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py
```

### ⚛️ Frontend Setup (React)

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Access the application at: http://localhost:3000

## 📂 Datasets

- **creditcard.csv** – Real anonymized dataset from European card transactions
- **fake_credit_card_dataset.json** – Synthetic test data for development

## 🧠 Model Training (Optional)

To retrain the model manually:

```bash
cd backend/app
python trainer.py
```

The model is saved as: `fraud_model.pkl`.

## 🔐 API Endpoints

| URL Endpoint        | Method | Purpose                   |
|---------------------|--------|---------------------------|
| /api/predict        | POST   | Predict fraud from transaction |
| /api/report-stolen  | POST   | Flag card as stolen       |
| /api/get-transactions | GET  | Fetch transaction logs    |

## 📈 Performance Metrics

| Metric              | Value  |
|---------------------|--------|
| Accuracy            | 99.2%  |
| Precision           | 95.7%  |
| Recall              | 94.3%  |
| F1 Score            | 95.0%  |
| AUC-ROC             | 0.987  |

## 🛡️ Security Guidelines for Deployment

- Enforce HTTPS for all connections
- Add Token-based Authentication for all API routes
- Replace JSON files with a relational database
- Implement event-based logging and alert system for suspicious activities
- Conduct regular security audits and penetration testing

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📱 Live Demo Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create a new Heroku app
heroku create fraud-detect-ai

# Push to Heroku
git push heroku main

# Open the deployed app
heroku open
```

### Docker Deployment

```bash
# Build Docker image
docker build -t fraud-detect-ai .

# Run Docker container
docker run -p 5000:5000 fraud-detect-ai
```

## 👨‍💻 Developed by

Bot-37  
Credit Card Fraud Defense Initiative – AI + Security Lab
