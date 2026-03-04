import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(page_title="AI4Govern", layout="wide")

st.title("AI4Govern – Public Procurement Risk Monitor")
st.write("AI-driven risk analytics for procurement oversight")

# =====================
# LOAD MODEL
# =====================
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "model.pkl")
    model = joblib.load(model_path)
    st.success("Model loaded successfully.")
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

    # Clean column names
    df.columns = df.columns.str.strip()

    # Rename columns to match training schema
    df.rename(columns={
        "Borrower Country / Economy": "Borrower Country"
    }, inplace=True)

    st.subheader("AI Model Prediction Engine")

    # =====================
    # FEATURE ENGINEERING
    # =====================
    try:
        # Contract Signing Year
        df["Contract Signing Date"] = pd.to_datetime(
            df["Contract Signing Date"], errors="coerce"
        )
        df["Contract Signing Year"] = df["Contract Signing Date"].dt.year

        # Contract Value Percentile
        df["Contract Value Percentile"] = (
            df["Supplier Contract Amount (USD)"].rank(pct=True)
        )

        # Repeat Supplier Flag
        supplier_counts = df["Supplier"].value_counts()
        df["Repeat Supplier Flag"] = (
            df["Supplier"].map(supplier_counts) > 1
        ).astype(int)

        # Contracts per Borrower Country
        if "Borrower Country" in df.columns:
            df["Contracts per Borrower Country"] = (
                df.groupby("Borrower Country")["WB Contract Number"]
                .transform("count")
            )
        else:
            df["Contracts per Borrower Country"] = 0

        # Contracts per Project Global Practice
        if "Project Global Practice" in df.columns:
            df["Contracts per Project Global Practice"] = (
                df.groupby("Project Global Practice")["WB Contract Number"]
                .transform("count")
            )
        else:
            df["Contracts per Project Global Practice"] = 0

    except Exception as e:
        st.error("Feature engineering failed.")
        st.write(e)
        st.stop()

    # =====================
    # HANDLE MISSING VALUES
    # =====================
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    categorical_cols = df.select_dtypes(include=["object"]).columns
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")

    # =====================
    # AI PREDICTION
    # =====================
    try:
        predictions = model.predict(df)
        probabilities = model.predict_proba(df)

        df["Risk Level"] = predictions
        df["Risk Confidence"] = probabilities.max(axis=1)

        st.success("AI-driven risk analysis completed successfully.")

    except Exception as e:
        st.error("Model prediction failed.")
        st.write(e)
        st.stop()

    # =====================
    # DASHBOARD
    # =====================
    st.markdown("## Key Risk Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contracts", f"{len(df):,}")
    col2.metric(
        "High Risk Contracts",
        f"{len(df[df['Risk Level'] == 'High']):,}",
    )
    col3.metric(
        "Average AI Risk Confidence",
        f"{df['Risk Confidence'].mean():.2f}",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Distribution")
        st.bar_chart(df["Risk Level"].value_counts())

    with col2:
        st.subheader("Risk Confidence Distribution")
        st.area_chart(df["Risk Confidence"])

    st.subheader("Top 10 High Risk Contracts")

    high_risk_df = (
        df[df["Risk Level"] == "High"]
        .sort_values(by="Risk Confidence", ascending=False)
        .head(10)
    )

    if not high_risk_df.empty:
        st.dataframe(high_risk_df)
    else:
        st.info("No High Risk contracts found.")

    # =====================
    # FEATURE IMPORTANCE
    # =====================
    st.subheader("Feature Importance")

    try:
        rf_model = model.named_steps["classifier"]
        importances = rf_model.feature_importances_

        if "preprocessor" in model.named_steps:
            feature_names = model.named_steps[
                "preprocessor"
            ].get_feature_names_out()
        else:
            feature_names = model.feature_names_in_

        fig, ax = plt.subplots(figsize=(10, 6))
        importances_series = pd.Series(importances, index=feature_names)
        top_features = importances_series.sort_values(ascending=False).head(15)

        top_features.sort_values().plot(kind="barh", ax=ax)

        st.pyplot(fig)

    except Exception:
        st.info("Feature importance not available.")
