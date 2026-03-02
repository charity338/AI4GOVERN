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
# LOAD TRAINED MODEL
# =====================
try:
    # Get absolute path for reliability on Streamlit Cloud
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "model.pkl")
    
    model = joblib.load(model_path)
    st.success("Model loaded successfully.")
    
    # Now that model exists, we can safely check its features
    with st.expander("View Model Training Features"):
        st.write(model.feature_names_in_)

except Exception as e:
    st.error("Model could not be loaded. Please ensure 'model.pkl' is in the repository.")
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
    # FEATURE ENGINEERING
    # =====================
    try:
        # Contract Signing Year
        df["Contract Signing Date"] = pd.to_datetime(df["Contract Signing Date"], errors="coerce")
        df["Contract Signing Year"] = df["Contract Signing Date"].dt.year

        # Contract Value Percentile
        df["Contract Value Percentile"] = df["Supplier Contract Amount (USD)"].rank(pct=True)

        # Repeat Supplier Flag
        supplier_counts = df["Supplier"].value_counts()
        df["Repeat Supplier Flag"] = (df["Supplier"].map(supplier_counts) > 1).astype(int)

        # Contracts per Borrower Country
        df["Contracts per Borrower Country"] = df.groupby("Borrower Country")["WB Contract Number"].transform("count")

        # Contracts per Project Global Practice
        df["Contracts per Project Global Practice"] = df.groupby("Project Global Practice")["WB Contract Number"].transform("count")
        
    except Exception as e:
        st.error("Feature engineering failed. Please check if your CSV has the correct column headers.")
        st.write(e)
        st.stop()

    # =====================
    # AI PREDICTIONS
    # =====================
    try:
        # Filter df to match the features used during training
        # This prevents "extra column" errors
        X_input = df[model.feature_names_in_]
        
        predictions = model.predict(X_input)
        probabilities = model.predict_proba(X_input)

        df["Risk Level"] = predictions
        df["Risk Confidence"] = probabilities.max(axis=1)

        st.success("AI-driven risk analysis completed successfully.")

    except Exception as e:
        st.error("Model prediction failed. This usually happens if columns are missing or named differently.")
        st.write(e)
        st.stop()

    # =====================
    # DASHBOARD METRICS
    # =====================
    st.markdown("## Key Risk Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contracts", f"{len(df):,}")
    
    # Logic to handle cases where 'High Risk' might not exist in the results
    high_risk_count = len(df[df['Risk Level'] == 'High Risk'])
    col2.metric("High Risk Contracts", f"{high_risk_count:,}")
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
        st.area_chart(df["Risk Confidence"])

    # =====================
    # TOP HIGH-RISK CONTRACTS
    # =====================
    st.subheader("Top 10 High Risk Contracts")
    high_risk_df = df[df["Risk Level"] == "High Risk"].sort_values(by="Risk Confidence", ascending=False).head(10)
    
    if not high_risk_df.empty:
        st.dataframe(high_risk_df)
    else:
        st.info("No 'High Risk' contracts identified in this dataset.")

    # =====================
    # FEATURE IMPORTANCE
    # =====================
    st.subheader("Feature Importance (Model Drivers)")

    try:
        # Assumes a Pipeline with a 'classifier' step (like RandomForest)
        rf_model = model.named_steps["classifier"]
        importances = rf_model.feature_importances_
        
        # Get feature names from the preprocessor if it exists
        if "preprocessor" in model.named_steps:
            feature_names = model.named_steps["preprocessor"].get_feature_names_out()
        else:
            feature_names = model.feature_names_in_

        fig, ax = plt.subplots(figsize=(10, 5))
        pd.Series(importances, index=feature_names).sort_values().plot(kind='barh', ax=ax)
        ax.set_xlabel("Importance Score")
        st.pyplot(fig)

    except Exception:
        st.info("Visual feature importance is not available for this specific model configuration.")
