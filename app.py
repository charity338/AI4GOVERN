import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# =====================
import os


# PAGE CONFIG
# =====================
st.set_page_config(page_title="AI4Govern", layout="wide")

st.title("AI4Govern – Public Procurement Risk Monitor")
st.write("AI-driven risk analytics for procurement oversight")

# =====================
# LOAD TRAINED MODEL
# =====================
try:
    model = joblib.load("model.pkl")
    st.write("Model loaded successfully.")
except Exception as e:
    st.error("Model could not be loaded.")
    st.write(e)
    st.stop()

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader("Upload Procurement Data (CSV)", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("AI Model Prediction Engine")

    # =====================
    # AI PREDICTIONS
    # =====================
    try:
        predictions = model.predict(df)
        probabilities = model.predict_proba(df)

        df["Risk Level"] = predictions
        df["Risk Confidence"] = probabilities.max(axis=1)

        st.success("AI-driven risk analysis completed successfully.")

    except Exception as e:
        st.error("Model prediction failed. Column mismatch likely.")
        st.write(e)
        st.stop()

    # =====================
    # DASHBOARD METRICS
    # =====================
    st.markdown("## Key Risk Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contracts", f"{len(df):,}")
    col2.metric("High Risk Contracts", f"{len(df[df['Risk Level'] == 'High Risk']):,}")
    col3.metric("Average AI Risk Confidence", f"{df['Risk Confidence'].mean():.2f}")

    # =====================
    # RISK DISTRIBUTION
    # =====================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Distribution")
        st.bar_chart(df["Risk Level"].value_counts())

    with col2:
        st.subheader("Risk Confidence Distribution")
        st.bar_chart(df["Risk Confidence"])

    # =====================
    # TOP HIGH-RISK CONTRACTS
    # =====================
    st.subheader("Top 10 High Risk Contracts")

    high_risk = df[df["Risk Level"] == "High Risk"] \
        .sort_values(by="Risk Confidence", ascending=False) \
        .head(10)

    st.dataframe(high_risk)

    # =====================
    # FEATURE IMPORTANCE
    # =====================
    st.subheader("Feature Importance (Model Drivers)")

    try:
        rf_model = model.named_steps["classifier"]
        importances = rf_model.feature_importances_
        feature_names = model.named_steps["preprocessor"].get_feature_names_out()

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(feature_names, importances)
        ax.set_xlabel("Importance Score")
        ax.set_title("Model Feature Importance")

        st.pyplot(fig)

    except:
        st.info("Feature importance not available for this model type.")
