import streamlit as st
import requests

st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="centered")
st.title("🏠 House Price Predictor (PyTorch + FastAPI)")

# You can change this if your API runs elsewhere
API_URL = "http://127.0.0.1:8000/predict"

CITY_TO_INDEX = {
    "Raleigh": 0,
    "Cary": 1,
    "Morrisville": 2,
    "Apex": 3,
    "Durham": 4,
    "Chapel Hill": 5,
    "Other": 6,
}

st.markdown("Enter the house features and click **Predict**.")

with st.form("predict_form", clear_on_submit=False):
    c1, c2 = st.columns(2)
    with c1:
        sqft = st.number_input("sqft", min_value=0.0, value=1800.0, step=100.0)
        bedrooms = st.number_input("bedrooms", min_value=0.0, value=3.0, step=1.0)
        bathrooms = st.number_input("bathrooms", min_value=0.0, value=2.0, step=0.5)
        age = st.number_input("age", min_value=0.0, value=10.0, step=1.0)
    with c2:
        floors = st.number_input("floors", min_value=0.0, value=2.0, step=1.0)
        garage = st.number_input("garage", min_value=0.0, value=1.0, step=1.0)
        lot_size = st.number_input("lot_size", min_value=0.0, value=4500.0, step=100.0)
        city_name = st.selectbox("city", options=list(CITY_TO_INDEX.keys()), index=0)

    submitted = st.form_submit_button("Predict")

if submitted:
    city_index = float(CITY_TO_INDEX[city_name])
    payload = {
        "sqft": sqft,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age": age,
        "floors": floors,
        "garage": garage,
        "lot_size": lot_size,
        "city_index": city_index,
    }

    with st.spinner("Calling API..."):
        try:
            resp = requests.post(API_URL, json=payload, timeout=10)
            if resp.ok:
                data = resp.json()
                price = data.get("predicted_price", None)
                if price is not None:
                    st.success(f"💰 Predicted Price: **{price:,.0f}**")
                else:
                    st.warning(f"Got response but no 'predicted_price' key: {data}")
            else:
                st.error(f"API error {resp.status_code}: {resp.text}")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")