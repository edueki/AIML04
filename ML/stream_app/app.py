import streamlit as st
import requests

# Replace with your model API endpoint
API_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="Loan Approval Predictor", page_icon="🏦")

st.title("🏦 Loan Approval Predictor")

st.write("Enter the applicant details below and click **Predict**.")

# Input fields
no_of_dependents = st.number_input(
    "Number of Dependents",
    min_value=0,
    max_value=20,
    value=2
)

education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

self_employed = st.selectbox(
    "Self Employed",
    ["Yes", "No"]
)

income_annum = st.number_input(
    "Annual Income",
    min_value=0,
    value=100000,
    step=1000
)

loan_amount = st.number_input(
    "Loan Amount",
    min_value=0,
    value=13333,
    step=1000
)

loan_term = st.number_input(
    "Loan Term (Months)",
    min_value=1,
    value=50
)

credit_score = st.slider(
    "Credit Score",
    min_value=300,
    max_value=900,
    value=650
)

total_assets_value = st.number_input(
    "Total Assets Value",
    min_value=0,
    value=650000,
    step=10000
)

if st.button("Predict Loan Approval"):
    payload = {
        "no_of_dependents": no_of_dependents,
        "education": education,
        "self_employed": self_employed,
        "income_annum": income_annum,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "credit_score": credit_score,
        "total_assets_value": total_assets_value,
    }

    with st.spinner("Getting prediction..."):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()

            result = response.json()

            st.success("Prediction received!")

            st.subheader("Result")
            st.json(result)

            # Optional: If your API returns {"loan_status": "Approved"}
            if "loan_status" in result:
                if result["loan_status"].lower() == "approved":
                    st.success("✅ Loan Approved")
                else:
                    st.error("❌ Loan Rejected")

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")

        except Exception as e:
            st.error(f"Unexpected Error: {e}")