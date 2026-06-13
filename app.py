import streamlit as st
import joblib

st.set_page_config(
    page_title="FinCheck AI",
    page_icon="💰",
    layout="wide"
)

model = joblib.load(
    "model.pkl"
)

st.title("💰 FinCheck AI")

income = st.number_input(
    "Monthly Income",
    0
)

expenses = st.number_input(
    "Monthly Expenses",
    0
)

savings = st.number_input(
    "Current Savings",
    0
)

goal_name = st.text_input(
    "Dream Goal"
)

goal_cost = st.number_input(
    "Goal Cost",
    0
)

if st.button("Analyze"):

    features = [[
        income,
        expenses,
        savings,
        goal_cost
    ]]

    prediction = model.predict(
        features
    )[0]

    probability = (
        model.predict_proba(
            features
        )[0][1]
        *100
    )

    surplus = income-expenses

    if surplus > 0:
        months = (
            goal_cost-savings
        )/surplus
    else:
        months = -1

    score = 0

    if income > 0:
        score = min(
            100,
            int(
                (surplus/income)
                *100
            )
        )

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Financial Health",
        f"{score}/100"
    )

    col2.metric(
        "Success Chance",
        f"{probability:.1f}%"
    )

    if months >= 0:
        col3.metric(
            "Months Needed",
            f"{months:.1f}"
        )

    progress = (
        savings/
        max(goal_cost,1)
    )*100

    st.progress(
        int(
            min(100,progress)
        )
    )

    if prediction == 1:
        st.success(
            f"Likely to achieve {goal_name}"
        )
    else:
        st.error(
            f"{goal_name} may be difficult currently"
        )

    if probability > 80:
        st.success(
            "Excellent financial position."
        )
    elif probability > 50:
        st.warning(
            "Moderate chance. Save more."
        )
    else:
        st.error(
            "High risk. Reduce expenses."
        )
