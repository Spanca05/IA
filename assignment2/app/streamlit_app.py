from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student At-Risk Demo",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #0f172a;
        --panel: #111827;
        --card: #1f2937;
        --accent: #38bdf8;
        --accent-2: #f59e0b;
        --text: #e5e7eb;
        --muted: #9ca3af;
    }
    .stApp {
        background: radial-gradient(circle at top left, rgba(56,189,248,0.16), transparent 30%),
                    radial-gradient(circle at top right, rgba(245,158,11,0.14), transparent 28%),
                    linear-gradient(180deg, #020617 0%, #0f172a 55%, #111827 100%);
        color: var(--text);
    }
    .hero {
        padding: 2rem 2.2rem 1.2rem 2.2rem;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        background: rgba(15,23,42,0.72);
        box-shadow: 0 18px 70px rgba(0,0,0,0.25);
        backdrop-filter: blur(14px);
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.6rem;
        line-height: 1.05;
    }
    .hero p {
        color: var(--muted);
        margin: 0.75rem 0 0 0;
        max-width: 60ch;
        font-size: 1.02rem;
    }
    .stat-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: rgba(17,24,39,0.88);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 12px 32px rgba(0,0,0,0.22);
    }
    .result-risk {
        padding: 1.1rem 1.2rem;
        border-radius: 18px;
        background: rgba(127,29,29,0.25);
        border: 1px solid rgba(248,113,113,0.45);
    }
    .result-safe {
        padding: 1.1rem 1.2rem;
        border-radius: 18px;
        background: rgba(6,78,59,0.25);
        border: 1px solid rgba(52,211,153,0.45);
    }
    .small-note {
        color: var(--muted);
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent
BUNDLE_PATH = BASE_DIR.parent / "models" / "student_risk_model.joblib"
RESULTS_DIR = BASE_DIR.parent / "results"
FALLBACK_MODEL_PATH = RESULTS_DIR / "LogisticRegression.joblib"
FALLBACK_SCALER_PATH = RESULTS_DIR / "scaler.joblib"

FEATURES = [
    "study_time_weekly",
    "absences",
    "sleep_hours",
    "stress_level",
    "parental_support",
    "tutoring",
    "extracurricular",
]

FEATURE_LABELS = {
    "study_time_weekly": "Study time weekly (hours)",
    "absences": "Absences",
    "sleep_hours": "Sleep hours",
    "stress_level": "Stress level (1-10)",
    "parental_support": "Parental support (0-4)",
    "tutoring": "Tutoring",
    "extracurricular": "Extracurricular",
}

@st.cache_resource
def load_artifacts():
    if BUNDLE_PATH.exists():
        bundle = joblib.load(BUNDLE_PATH)
        return bundle["model_name"], bundle["model"], bundle.get("scaler"), bundle.get("feature_names", FEATURES)

    model = joblib.load(FALLBACK_MODEL_PATH)
    scaler = joblib.load(FALLBACK_SCALER_PATH) if FALLBACK_SCALER_PATH.exists() else None
    return "LogisticRegression", model, scaler, FEATURES


def build_input_frame() -> pd.DataFrame:
    col1, col2 = st.columns(2)

    with col1:
        study_time = st.slider("Study time weekly (hours)", 0.0, 30.0, 12.0, 0.5)
        sleep_hours = st.slider("Sleep hours", 3.0, 10.0, 7.0, 0.1)
        parental_support = st.slider("Parental support", 0, 4, 2, 1)
        tutoring = st.selectbox("Tutoring", ["No", "Yes"], index=0)

    with col2:
        absences = st.slider("Absences", 0, 20, 5, 1)
        stress_level = st.slider("Stress level", 1, 10, 5, 1)
        extracurricular = st.selectbox("Extracurricular", ["No", "Yes"], index=1)

    payload = pd.DataFrame(
        [
            {
                "study_time_weekly": study_time,
                "absences": absences,
                "sleep_hours": sleep_hours,
                "stress_level": stress_level,
                "parental_support": parental_support,
                "tutoring": 1 if tutoring == "Yes" else 0,
                "extracurricular": 1 if extracurricular == "Yes" else 0,
            }
        ],
        columns=FEATURES,
    )
    return payload


st.markdown(
    """
    <div class="hero">
        <h1>Student At-Risk Prediction</h1>
        <p>Enter a university student's profile and the trained model estimates whether the student is at risk of failing the academic year or dropping out.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

model_name, model, scaler, feature_names = load_artifacts()

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.subheader("Input profile")
    input_df = build_input_frame()
    predict = st.button("Predict", type="primary", use_container_width=True)

with right:
    st.subheader("Model info")
    st.markdown(
        f"""
        <div class="stat-card">
            <strong>Active model</strong><br />
            {model_name}<br /><br />
            <span class="small-note">Input features</span><br />
            {", ".join(feature_names)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="stat-card" style="margin-top: 1rem;">
            <strong>Interpretation</strong><br />
            Higher study time and support usually lower the risk score, while more absences and stress tend to increase it.
        </div>
        """,
        unsafe_allow_html=True,
    )

if predict:
    features = input_df[feature_names]
    if scaler is not None:
        features_for_model = pd.DataFrame(
            scaler.transform(features),
            columns=feature_names,
            index=features.index,
        )
    else:
        features_for_model = features

    proba = float(model.predict_proba(features_for_model)[0, 1])
    label = int(proba >= 0.5)
    result_text = "At Risk of Dropout / Year Failure" if label == 1 else "Not At Risk"

    with st.container():
        if label == 1:
            st.markdown(
                f"""
                <div class="result-risk">
                    <h3 style="margin: 0 0 0.4rem 0;">Prediction: At Risk of Dropout / Year Failure</h3>
                    <p style="margin: 0;">Estimated risk probability: <strong>{proba:.1%}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-safe">
                    <h3 style="margin: 0 0 0.4rem 0;">Prediction: Not At Risk</h3>
                    <p style="margin: 0;">Estimated risk probability: <strong>{proba:.1%}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.caption(f"Decision threshold: 0.50 | Raw label: {result_text}")
else:
    st.info("Adjust the inputs and click Predict to estimate the risk level.")

st.markdown(
    """
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.08); color: #9ca3af; font-size: 0.85rem; text-align: center;">
        Prototype developed for AI Assignment 2
    </div>
    """,
    unsafe_allow_html=True,
)
