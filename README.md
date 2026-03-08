# ✈️ Voyage Analytics: AI Travel Cost Prediction Platform

Voyage Analytics is an end-to-end Machine Learning platform that predicts travel costs using historical data and machine learning models.  
The system provides an API for price prediction and an interactive dashboard for users to estimate travel expenses based on different parameters.

The project demonstrates how machine learning models can be deployed in a production-like environment using APIs, dashboards, and containerization.

---

## 🚀 Live Demo

API Documentation (Swagger UI)

http://localhost:8000/docs

Streamlit Dashboard

http://localhost:8501

---

## 🧠 Problem Statement

Planning travel involves estimating costs such as flights and hotels, which vary depending on distance, class, location, and other factors.

Travelers often struggle to estimate these costs quickly.

Voyage Analytics solves this problem by building a machine learning model that predicts travel prices and exposes it through a scalable API and interactive dashboard.

---

## 🏗️ System Architecture

User  
↓  
Streamlit Dashboard  
↓  
FastAPI REST API  
↓  
Machine Learning Model (Scikit-Learn)  
↓  
MLflow Experiment Tracking  

---

## ⚙️ Tech Stack

- Python
- Pandas
- Scikit-Learn
- FastAPI
- Streamlit
- MLflow
- Docker
- Git
- REST APIs

---

## 📂 Project Structure
voyage-analytics
│
├── app
│ ├── app.py
│ ├── schemas.py
│ └── utils.py
│
├── models
│ ├── flight_model.pkl
│ └── hotel_model.pkl
│
├── streamlit_app
│ └── dashboard.py
│
├── notebooks
│ └── model_training.ipynb
│
├── mlruns
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md


---

## ✨ Features

- Flight price prediction
- Hotel price estimation
- Distance calculation using geolocation
- Machine learning experiment tracking
- REST API for predictions
- Interactive Streamlit dashboard
- Dockerized deployment
- Production-ready project structure

---

## 🧪 Example API Request

Endpoint

---

## ✨ Features

- Flight price prediction
- Hotel price estimation
- Distance calculation using geolocation
- Machine learning experiment tracking
- REST API for predictions
- Interactive Streamlit dashboard
- Dockerized deployment
- Production-ready project structure

---

## 🧪 Example API Request

Endpoint
POST /predict


Example Request

json
{
  "source": "Delhi",
  "destination": "Mumbai",
  "distance_km": 1150,
  "travel_class": "Economy"
}

Example Response

{
  "predicted_price": 5420
}
🐳 Running the Project with Docker

Clone the repository


git clone https://github.com/YOUR_USERNAME/voyage-analytics.git


Go to the project directory


cd voyage-analytics


Run the application


docker-compose up --build

🌐 Access the Services
Service	URL
FastAPI API	http://localhost:8000/docs

Streamlit Dashboard	http://localhost:8501

MLflow Tracking	http://localhost:5001
📊 Machine Learning Workflow

Data collection and preprocessing

Feature engineering

Model training using Scikit-Learn

Experiment tracking with MLflow

Model serialization with Joblib

API deployment with FastAPI

UI integration with Streamlit

Containerization using Docker

📈 Future Improvements

Add real-time flight and hotel APIs

Improve model accuracy using advanced algorithms

Add recommendation system for destinations

Deploy the platform on cloud infrastructure

Add user authentication and booking features

👩‍💻 Author

Shreya Sachan

Aspiring Data Scientist / Machine Learning Engineer

⭐ If you found this project useful

Please consider giving the repository a star on GitHub!
