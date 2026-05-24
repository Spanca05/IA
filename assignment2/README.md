# Student At-Risk Prediction

## Project Overview

This project aims to analyze university student lifestyle and academic behavior data in order to identify students who are at risk of failing the academic year or dropping out.

Using a synthetic dataset containing factors such as study time, absences, sleep habits, stress levels, parental support, tutoring, and extracurricular activities, the project explores how different variables may influence student performance and academic risk levels.

The project focuses on applying data science and machine learning techniques to better understand student-related patterns and predict whether a student may be considered at risk.

---

## Dataset

The dataset was synthetically generated for educational and machine learning purposes.

It contains multiple features related to student behavior, lifestyle, and support systems.

### Dataset Features

| Feature | Description |
|---|---|
| `student_id` | Unique identifier for each student |
| `study_time_weekly` | Weekly study time in hours |
| `absences` | Number of absences |
| `sleep_hours` | Average sleep hours per night |
| `stress_level` | Self-reported stress level (1–10) |
| `parental_support` | Level of parental support (0–4) |
| `tutoring` | Whether the student receives tutoring (0/1) |
| `extracurricular` | Participation in extracurricular activities (0/1) |
| `at_risk` | Target variable indicating risk of year failure or dropout (0/1) |

### Target Variable

| Value | Meaning |
|---|---|
| `0` | Student is not at risk of year failure or dropout |
| `1` | Student is at risk of failing the academic year or dropping out |

---

## Project Goals

The main objectives of this project are:

- Perform Exploratory Data Analysis (EDA)
- Identify patterns and correlations in the dataset
- Visualize important trends and distributions
- Prepare and preprocess the data
- Train and compare machine learning models
- Evaluate model performance
- Understand which factors contribute most to academic risk

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib & Seaborn
- Scikit-learn
- Jupyter Notebook
- Streamlit (web demo)

---

## Getting Started

### Prerequisites

1. Python 3.9+ installed
2. Virtual environment created and activated
3. Dependencies installed: `pip install pandas numpy matplotlib seaborn scikit-learn jupyter streamlit`

### How to Run

The project follows a complete pipeline from data generation to interactive prediction:

#### Step 1: Generate the Dataset
```bash
python assignment2/data/generate_dataset.py
```
This creates `assignment2/data/students_dataset.csv` with 1000 synthetic student records.

#### Step 2: Train the Model
Open and run the notebook `assignment2/notebooks/02_model_training.ipynb`:
- Loads the generated dataset
- Applies proper scaling (prevents data leakage)
- Trains and compares three models: Logistic Regression, Decision Tree, Random Forest
- Evaluates with multiple metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
- Saves trained artifacts:
  - `assignment2/models/student_risk_model.joblib` (bundled model)
  - `assignment2/models/scaler.joblib` (StandardScaler)
  - Model comparison metrics in `assignment2/results/`

**Note:** This notebook must be run before launching the app, as the app depends on the trained model artifacts.

#### Step 3: Launch the Interactive Web App
```bash
streamlit run assignment2/app/streamlit_app.py
```
The app provides an interactive interface to:
- Input student features via sliders and selectors
- Get real-time risk predictions
- View probability of academic risk

---

## Project Structure

```text
assignment2/
│
├── data/              # Dataset files
│   └── generate_dataset.py     # Dataset generation script
├── notebooks/         # Jupyter notebooks
│   ├── 01_eda.ipynb            # Exploratory Data Analysis
│   └── 02_model_training.ipynb # Model training & artifact generation
├── app/               # Streamlit web application
│   ├── streamlit_app.py        # Main app
│   └── README.md               # App documentation
├── models/            # Generated model artifacts (.joblib)
├── results/           # Evaluation results & metrics
└── README.md
```

---

## Workflow Diagram

```
generate_dataset.py → students_dataset.csv
                          ↓
                    01_eda.ipynb (optional, for analysis)
                          ↓
                    02_model_training.ipynb
                          ↓
                    *.joblib files (models, scaler)
                          ↓
                    streamlit_app.py
                          ↓
                    Interactive web interface
```

---

## Model Performance

The best-performing model (Logistic Regression) achieved:
- **Accuracy:** 78.50%
- **Precision:** 71.19%
- **Recall:** 61.76%
- **F1-Score:** 66.14%
- **ROC-AUC:** 85.09%

Key finding: **Weekly study time** is the strongest negative predictor of academic risk (correlation: -0.42).

---

## Important Notes

1. **Data Leakage Prevention:** The model uses proper train/test split before scaling, ensuring scalers are fit only on training data.

2. **Artifact Generation:** Model artifacts (`.joblib` files) are generated when running `02_model_training.ipynb` and are required for the app to function.

3. **Feature Scaling:** The app automatically scales user inputs using the same StandardScaler fitted during training.

4. **Reproducibility:** All results are deterministic with `random_state=42` for train/test split and model initialization.

---

## Academic Context

Artificial Intelligence - Assignment 2

Faculty of Engineering, University of Porto (FEUP)