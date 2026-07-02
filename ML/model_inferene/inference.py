import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import uvicorn
import sklearn
import numpy as np
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
app = FastAPI()

model = joblib.load('model.pkl')

class RequestData(BaseModel):
    no_of_dependents: int
    education: str
    self_employed: str
    income_annum: float
    loan_amount: float
    loan_term: float
    credit_score: int
    total_assets_value: float

@app.post("/predict")
def predict(data: RequestData):

    dataset = {
        "no_of_dependents": data.no_of_dependents,
        "education": data.education,
        "self_employed": data.self_employed,
        "income_annum": data.income_annum,
        "loan_amount": data.loan_amount,
        "loan_term": data.loan_term,
        "credit_score": data.credit_score,
        "total_assets_value": data.total_assets_value
    }
    data_df = pd.DataFrame([dataset])
    # Input features Encoding
    data_df['education'] = le.fit_transform(data_df['education'])
    data_df['self_employed'] = le.fit_transform(data_df['self_employed'])
    # numpy log form
    log_columns = ['income_annum', 'loan_amount', 'total_assets_value']
    data_df[log_columns] = np.log(data_df[log_columns])

    print (type(data_df.head()))
    predictions = int(model.predict(data_df)[0])

    predictions_decoded = "Approved" if predictions == 1 else "Not Approved"

    return {"Loan Status": predictions_decoded }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


