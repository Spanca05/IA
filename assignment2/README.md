# Student At-Risk Prediction

## Project Overview

This project aims to analyze student lifestyle and academic behavior data in order to identify students who may be academically at risk.

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
| `at_risk` | Target variable indicating academic risk (0/1) |

### Target Variable

| Value | Meaning |
|---|---|
| `0` | Student is not considered at risk |
| `1` | Student is considered at risk |

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
- Matplotlib
- Scikit-learn
- Jupyter Notebook

---

## Project Structure

```text
project/
│
├── data/              # Dataset files
├── notebooks/         # Jupyter notebooks
├── src/               # Source code
├── README.md