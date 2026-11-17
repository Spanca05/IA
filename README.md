# Artificial Intelligence Projects

Two projects developed for the Artificial Intelligence course at FEUP (University of Porto), 2025/2026.

| Project | Topic | Stack |
|---|---|---|
| [Self-Driving Rides Optimizer](#1-self-driving-rides-optimizer) | Optimisation / metaheuristics | Python · Streamlit · pandas · matplotlib |
| [Student At-Risk Prediction](#2-student-at-risk-prediction) | Data science / machine learning | Python · pandas · scikit-learn · Streamlit |

---

## 1. Self-Driving Rides Optimizer

Optimisation of ride assignments for a fleet of autonomous vehicles (Google Hash Code–style problem).

### Overview
Given a city grid, a fleet of vehicles and a list of rides with time windows, the goal is to assign rides to vehicles to maximise the total score (distance travelled on time plus a bonus for starting exactly on time).

### Features
- **Four optimisation algorithms:** Greedy, Hill Climbing, Simulated Annealing and Genetic Algorithm
- **Warm and cold start** for Hill Climbing and Simulated Annealing (start from the greedy solution or from a random one)
- **Interactive Streamlit GUI**
  - *Single Execution:* run one algorithm on an instance, tune its parameters and see the routes drawn on a map
  - *Algorithms Comparison:* run several algorithms and compare average score and runtime
- **Benchmark script** for batch experiments from the terminal

### How to run
```bash
pip install streamlit pandas matplotlib
cd project/src
python -m streamlit run gui.py
```
Terminal version: `python project/src/main.py` · Benchmark: `python project/src/benchmark.py --runs 10 --seed 42`

### Project structure
`parser.py` (input) · `solvers.py` (algorithm dispatcher) · `greedy.py`, `hill_climbing.py`, `simulated_annealing.py`, `genetic_algorithm.py` · `neighborhood.py` (neighbour operators) · `evaluator.py` / `simulation.py` (scoring) · `gui.py` (Streamlit interface)

More details in [`project/README.md`](project/README.md).

---

## 2. Student At-Risk Prediction

End-to-end machine learning pipeline that predicts whether a university student is at risk of failing the academic year or dropping out.

### Overview
- **Data:** synthetic dataset of 1,000 students (study time, absences, sleep, stress, parental support, tutoring, extracurricular activities)
- **Exploratory data analysis:** distributions, correlations and key risk factors
- **Modelling:** Logistic Regression, Decision Tree and Random Forest with scikit-learn, with scaling applied after the train/test split to prevent data leakage
- **Evaluation:** accuracy, precision, recall, F1 and ROC-AUC. The best model (Logistic Regression) reached **78.5% accuracy** and **0.85 ROC-AUC**
- **Web app:** Streamlit interface where users enter a student's indicators and get a real-time risk prediction and probability

### How to run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter streamlit
cd assignment2
python data/generate_dataset.py          # 1. generate the dataset
jupyter notebook notebooks/02_model_training.ipynb   # 2. train the models (run all cells)
streamlit run app/streamlit_app.py       # 3. launch the web app
```

More details in [`assignment2/README.md`](assignment2/README.md).

---

## Authors
Vasco Vieira · Leonardo Carvalho · Guilherme Gamelas
