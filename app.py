app.py


import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI4Govern", layout="wide")

st.title("AI4Govern – Public Procurement Risk Monitor")
st.write("AI-driven risk analytics for procurement oversight")

uploaded_file = st.file_uploader("Upload Procurement Data (CSV)", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Convert date
    df["Contract Signing Date"] = pd.to_datetime(
        df["Contract Signing Date"], errors="coerce"
    )

    # Create Signing Year
    df["Signing Year"] = df["Contract Signing Date"].dt.year

    # Contract value percentile
    df["Contract Value Percentile"] = (
        df["Supplier Contract Amount (USD)"].rank(pct=True) * 100
    )

    # Repeat supplier flag
    df["Repeat Supplier"] = df.duplicated(subset=["Supplier"], keep=False)

    # Contracts per Global Practice
    df["Contracts per Practice"] = df.groupby(
        "Project Global Practice"
    )["WB Contract Number"].transform("count")

    # Risk Classification Logic
    def classify_risk(row):
        if row["Contract Value Percentile"] >= 75 and not row["Repeat Supplier"]:
            return "High Risk"
        elif row["Contract Value Percentile"] < 50 and row["Repeat Supplier"]:
            return "Low Risk"
        else:
            return "Medium Risk"

    df["Risk Level"] = df.apply(classify_risk, axis=1)

    st.success("Risk analysis completed.")

    # =====================
    # DASHBOARD SECTION
    # =====================

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Distribution")
        st.bar_chart(df["Risk Level"].value_counts())

    with col2:
        st.subheader("Risk by Global Practice")
        st.bar_chart(
            df.groupby("Project Global Practice")["Risk Level"]
            .value_counts()
            .unstack()
            .fillna(0)
        )

    st.subheader("Top 10 High Risk Contracts")
    high_risk = df[df["Risk Level"] == "High Risk"].sort_values(
        by="Supplier Contract Amount (USD)", ascending=False
    ).head(10)

    st.dataframe(
        high_risk[
            [
                "Project Name",
                "Supplier",
                "Supplier Contract Amount (USD)",
                "Project Global Practice",
                "Signing Year",
            ]
        ]
    )

    st.subheader("Risk by Year")
    st.bar_chart(
        df.groupby("Signing Year")["Risk Level"]
        .value_counts()
        .unstack()
        .fillna(0)
    )
