import streamlit as st
import joblib

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="FinCheck AI",
    page_icon="💰",
    layout="centered"
)

model = joblib.load("model.pkl")

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
    background:white;
    color:black;
}

*{
    color:black !important;
}

.main-title{
    font-size:3.5rem;
    font-weight:900;
    text-align:center;
    color:#16a34a !important;
}

.subtitle{
    text-align:center;
    font-size:1.1rem;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">
💰 FinCheck AI
</div>

<div class="subtitle">
Track Finances • Build Dreams
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Financial Health",
        "🎯 Dream Vault"
    ]
)

# ==================================================
# FINANCIAL HEALTH PAGE
# ==================================================

if page == "📊 Financial Health":

    st.header("📊 Financial Dashboard")

    st.subheader("💵 Income Sources")

    salary = st.number_input(
        "Salary",
        min_value=0
    )

    freelance = st.number_input(
        "Freelancing",
        min_value=0
    )

    other_income = st.number_input(
        "Other Income",
        min_value=0
    )

    total_income = (
        salary +
        freelance +
        other_income
    )

    st.success(
        f"Total Income: ₹{total_income}"
    )

    st.subheader("💸 Expense Sources")

    food = st.number_input(
        "Food",
        min_value=0
    )

    transport = st.number_input(
        "Transport",
        min_value=0
    )

    entertainment = st.number_input(
        "Entertainment",
        min_value=0
    )

    education = st.number_input(
        "Education",
        min_value=0
    )

    other_expenses = st.number_input(
        "Other Expenses",
        min_value=0
    )

    total_expenses = (
        food +
        transport +
        entertainment +
        education +
        other_expenses
    )

    st.error(
        f"Total Expenses: ₹{total_expenses}"
    )

    st.subheader("🏦 Savings")

    savings = st.number_input(
        "Current Savings",
        min_value=0
    )

    if st.button("🚀 Analyze Financial Health"):

        features = [[
            total_income,
            total_expenses,
            savings,
            50000
        ]]

        probability = (
            model.predict_proba(
                features
            )[0][1]
            * 100
        )

        surplus = (
            total_income -
            total_expenses
        )

        if total_income > 0:

            score = int(
                max(
                    0,
                    min(
                        100,
                        (surplus /
                         total_income)
                        * 100
                    )
                )
            )

        else:
            score = 0

        st.divider()

        c1,c2,c3 = st.columns(3)

        c1.metric(
            "💚 Health Score",
            f"{score}/100"
        )

        c2.metric(
            "💰 Monthly Surplus",
            f"₹{surplus}"
        )

        c3.metric(
            "🎯 Success Index",
            f"{probability:.1f}%"
        )

        if score >= 75:

            st.success(
                "Excellent Financial Health"
            )

        elif score >= 50:

            st.warning(
                "Average Financial Health"
            )

        else:

            st.error(
                "Needs Improvement"
            )

# ==================================================
# DREAM VAULT PAGE
# ==================================================

elif page == "🎯 Dream Vault":

    st.header("🎯 Dream Vault")

    dream_name = st.text_input(
        "Dream Name"
    )

    dream_cost = st.number_input(
        "Dream Cost (₹)",
        min_value=0
    )

    current_savings = st.number_input(
        "Savings Available (₹)",
        min_value=0
    )

    monthly_saving = st.number_input(
        "Monthly Saving Amount (₹)",
        min_value=0
    )

    if st.button("✨ Analyze Dream"):

        if monthly_saving > 0:

            months = (
                max(
                    0,
                    dream_cost -
                    current_savings
                )
                /
                monthly_saving
            )

            progress = (
                current_savings /
                max(dream_cost,1)
            ) * 100

            st.metric(
                "⏳ Months Needed",
                f"{months:.1f}"
            )

            st.progress(
                min(
                    int(progress),
                    100
                )
            )

            st.write(
                f"Progress: {progress:.1f}%"
            )

            if months <= 3:

                st.success(
                    f"You can achieve {dream_name} very soon!"
                )

            elif months <= 12:

                st.warning(
                    f"{dream_name} is achievable within a year."
                )

            else:

                st.error(
                    f"{dream_name} needs long-term planning."
                )

        else:

            st.error(
                "Monthly saving must be greater than zero."
            )

st.divider()
st.caption("💰 FinCheck ")
