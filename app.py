# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="AI4Govern", layout="wide")

# st.title("AI4Govern – Public Procurement Risk Monitor")
# st.write("AI-driven risk analytics for procurement oversight")

# uploaded_file = st.file_uploader("Upload Procurement Data (CSV)", type=["csv"])

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)

#     st.sidebar.header("Dashboard Filters")

#     practice_filter = st.sidebar.multiselect(
#         "Select Global Practice",
#         options=df["Project Global Practice"].dropna().unique(),
#         default=df["Project Global Practice"].dropna().unique()
#     )

#     df = df[df["Project Global Practice"].isin(practice_filter)]

#     # Convert date
#     df["Contract Signing Date"] = pd.to_datetime(
#         df["Contract Signing Date"], errors="coerce"
#     )

#     # Create Signing Year
#     df["Signing Year"] = df["Contract Signing Date"].dt.year

#     # Contract value percentile
#     df["Contract Value Percentile"] = (
#         df["Supplier Contract Amount (USD)"].rank(pct=True) * 100
#     )

#     # Repeat supplier flag
#     df["Repeat Supplier"] = df.duplicated(subset=["Supplier"], keep=False)

#     # Contracts per Global Practice
#     df["Contracts per Practice"] = df.groupby(
#         "Project Global Practice"
#     )["WB Contract Number"].transform("count")

#     # Risk Classification Logic
#     def classify_risk(row):
#         if row["Contract Value Percentile"] >= 75 and not row["Repeat Supplier"]:
#             return "High Risk"
#         elif row["Contract Value Percentile"] < 50 and row["Repeat Supplier"]:
#             return "Low Risk"
#         else:
#             return "Medium Risk"

#     df["Risk Level"] = df.apply(classify_risk, axis=1)

#     st.success("Risk analysis completed.")

#     # =====================
#     # DASHBOARD SECTION
#     # =====================
#     st.markdown("## Key Risk Indicators")

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Contracts", f"{len(df):,}")
#     col2.metric("High Risk Contracts", f"{len(df[df['Risk Level']=='High Risk']):,}")
#     col3.metric("Total Financial Exposure (USD)", f"${df['Supplier Contract Amount (USD)'].sum():,.0f}")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.subheader("Risk Distribution")
#         st.bar_chart(df["Risk Level"].value_counts())

#     with col2:
#         st.subheader("Risk by Global Practice")
#         st.bar_chart(
#             df.groupby("Project Global Practice")["Risk Level"]
#             .value_counts()
#             .unstack()
#             .fillna(0)
#         )

#     st.subheader("Top 10 High Risk Contracts")
#     high_risk = df[df["Risk Level"] == "High Risk"].sort_values(
#         by="Supplier Contract Amount (USD)", ascending=False
#     ).head(10)
#     st.dataframe(
#         high_risk[
#             [
#                 "Project Name",
#                 "Supplier",
#                 "Supplier Contract Amount (USD)",
#                 "Project Global Practice",
#                 "Signing Year",
#             ]
#         ]
#     )

#     st.subheader("Risk by Year")
#     st.bar_chart(
#         df.groupby("Signing Year")["Risk Level"]
#         .value_counts()
#         .unstack()
#         .fillna(0)
#     )


import streamlit as st
import pandas as pd

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(page_title="AI4Govern", layout="wide")

st.title("AI4Govern – Public Procurement Risk Monitor")
st.write("AI-driven risk analytics for procurement oversight")

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader("Upload Procurement Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # =====================
    # DASHBOARD FILTERS
    # =====================
    st.sidebar.header("Dashboard Filters")

    practice_filter = st.sidebar.multiselect(
        "Select Global Practice",
        options=df["Project Global Practice"].dropna().unique(),
        default=df["Project Global Practice"].dropna().unique()
    )

    df = df[df["Project Global Practice"].isin(practice_filter)]

    # =====================
    # DATA PREPROCESSING
    # =====================
    # Convert contract signing date to datetime
    df["Contract Signing Date"] = pd.to_datetime(df["Contract Signing Date"], errors="coerce")
    df["Signing Year"] = df["Contract Signing Date"].dt.year

    # Contract value percentile
    df["Contract Value Percentile"] = df["Supplier Contract Amount (USD)"].rank(pct=True) * 100

    # Repeat supplier flag
    supplier_counts = df["Supplier"].value_counts()
    df["Repeat Supplier"] = df["Supplier"].map(supplier_counts) > 1  # True if appears >1

    # Contracts per Global Practice
    df["Contracts per Practice"] = df.groupby("Project Global Practice")["WB Contract Number"].transform("count")

    # =====================
    # RISK CLASSIFICATION
    # =====================
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
    # DASHBOARD METRICS
    # =====================
    st.markdown("## Key Risk Indicators")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Contracts", f"{len(df):,}")
    col2.metric("High Risk Contracts", f"{len(df[df['Risk Level'] == 'High Risk']):,}")
    col3.metric("Total Financial Exposure (USD)", f"${df['Supplier Contract Amount (USD)'].sum():,.0f}")

    # =====================
    # RISK DISTRIBUTION CHARTS
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

    # =====================
    # HIGH RISK CONTRACTS TABLE
    # =====================
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

    # =====================
    # RISK BY YEAR
    # =====================
    st.subheader("Risk by Signing Year")
    risk_by_year = df.groupby("Signing Year")["Risk Level"].value_counts().unstack().fillna(0)

    # Color-coded styling
    def highlight_risk(val):
        color = ""
        if val.name == "High Risk":
            color = "background-color: #ff4c4c; color: white"  # red
        elif val.name == "Medium Risk":
            color = "background-color: #ffcc00; color: black"   # yellow
        elif val.name == "Low Risk":
            color = "background-color: #00b300; color: white"   # green
        return [color] * len(val)

    styled_df = risk_by_year.style.apply(highlight_risk, axis=0)
    st.dataframe(styled_df)

    # =====================
    # SUPPLIER FLAG INSIGHTS
    # =====================
    st.subheader("Supplier Risk Patterns")
    st.write(
        "Suppliers appearing more than once are flagged as potentially lower risk; "
        "unique suppliers may indicate higher risk if combined with high contract values."
    )
    st.dataframe(
        df.groupby("Supplier")["Repeat Supplier"].agg(["count", "first"]).sort_values(by="count", ascending=False)
    )
