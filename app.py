import streamlit as st
import pandas as pd
import joblib

st.title("Titanic Survival Prediction")
st.write(
    "Enter passenger information to predict the survival probability using a machine learning model trained on the Titanic dataset."
)

model = joblib.load("titanic_model.pkl")
columns = joblib.load("titanic_columns.pkl")

pclass = st.selectbox("Passenger Class", [1, 2, 3])
sex = st.selectbox("Sex", ["male", "female"])
age = st.slider("Age", 0, 80, 30)
sibsp = st.number_input("SibSp", 0, 10, 0)
parch = st.number_input("Parch", 0, 10, 0)
fare = st.number_input("Fare", 0.0, 600.0, 50.0)
embarked = st.selectbox("Embarked", ["C", "Q", "S"])

input_input_df = pd.DataFrame({
    "Pclass": [pclass],
    "Age": [age],
    "SibSp": [sibsp],
    "Parch": [parch],
    "Fare": [fare],
    "Sex_female": [1 if sex == "female" else 0],
    "Sex_male": [1 if sex == "male" else 0],
    "Embarked_C": [1 if embarked == "C" else 0],
    "Embarked_Q": [1 if embarked == "Q" else 0],
    "Embarked_S": [1 if embarked == "S" else 0],
})

input_df = input_input_df[columns]

st.write("Input data")
st.dataframe(input_input_df)

if st.button("Predict"):
    prob = model.predict_proba(input_df)[0, 1]

    st.subheader("Prediction Result")
    st.metric("Survival Probability", f"{prob * 100:.1f}%")

    if prob >= 0.5:
        st.success("Predicted: Survived")
    else:
        st.error("Predicted: Did not survive")
