import streamlit as st
import joblib

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="FinCheck AI",
    page_icon="💰",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------

model = joblib.load("model.pkl")

# ---------------- CSS ----------------

st.markdown("""
<style>

/* Background */
.stApp{
    background:white;
}

/* Title */
.main-title{
    font-size:4rem;
    font-weight:900;
    text-align:center;
    color:#16a34a;
    margin-bottom:0;
}

.subtitle{
    text-align:center;
    color:#64748b;
    font-size:1.2rem;
    margin-bottom:25px;
}

/* Headings */
h1,h2,h3,h4{
    color:#0f172a !important;
}

/* Labels */
label{
    color:#0f172a !important;
    font-weight:700 !important;
}

/* Number Inputs */
.stNumberInput input{
    background:#0f172a !important;
    color:white !important;
    border:2px solid #16a34a !important;
    border-radius:12px !important;
    font-weight:700 !important;
}

/* Text Inputs */
.stTextInput input{
    background:#0f172a !important;
    color:white !important;
    border:2px solid #16a34a !important;
    border-radius:12px !important;
    font-weight:700 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div{
    background:#0f172a !important;
    color:white !important;
    border:2px solid #16a34a !important;
    border-radius:12px !important;
}

div[data-baseweb="select"] *{
    color:white !important;
}

/* Metrics */
[data-testid="stMetricLabel"]{
    color:#64748b !important;
}

[data-testid="stMetricValue"]{
    color:#16a34a !important;
    font-weight:800 !important;
}

/* Paragraphs */
p{
    color:#334155 !important;
}

/* Button */
.stButton > button{
    background:#16a34a !important;
    color:white !important;
    border:none !important;
    border-radius:12px !important;
    font-weight:700 !important;
    width:100%;
    height:50px;
}

.stButton > button:hover{
    background:#15803d !important;
}

/* Floating Money */
.money{
    position:fixed;
    font-size:35px;
    pointer-events:none;
    z-index:999;
    animation:floatMoney linear infinite;
}

.m1{
    left:5%;
    animation-duration:12s;
}

.m2{
    left:25%;
    animation-duration:18s;
}

.m3{
    left:45%;
    animation-duration:15s;
}

.m4{
    left:65%;
    animation-duration:20s;
}

.m5{
    left:85%;
    animation-duration:14s;
}

@keyframes floatMoney{
    from{
        top:110%;
        transform:rotate(0deg);
    }

    to{
        top:-20%;
        transform:rotate(360deg);
    }
}

</style>

<div class="money m1">💸</div>
<div class="money m2">💵</div>
<div class="money m3">💰</div>
<div class="money m4">💸</div>
<div class="money m5">💵</div>

""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="main-title">
💰 FinCheck AI
</div>

<div class="subtitle">
Track Finances • Build Dreams • Make Better Decisions
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUTS ----------------

income = st.number_input(
    "Monthly Income (₹)",
    min_value=0,
    step=1000
)

expenses = st.number_input(
    "Monthly Expenses (₹)",
    min_value=0,
    step=1000
)

savings = st.number_input(
    "Current Savings (₹)",
    min_value=0,
    step=1000
)

goal_name = st.selectbox(
    "Choose Your Dream",
    [
        "🎸 Guitar",
        "💻 Laptop",
        "🏍️ Bike",
        "✈️ Vacation",
        "📱 Phone",
        "🚗 Car",
        "🏠 House"
    ]
)

goal_cost = st.number_input(
    "Dream Cost (₹)",
    min_value=0,
    step=1000
)
target_days = st.number_input(
    "🎯 Days Until You Want This Dream",
    min_value=1,
    value=90,
    step=1
)

st.write("")

analyze = st.button("🚀 Analyze")

# ---------------- RESULTS ----------------
# ---------------- RESULTS ----------------

if analyze:

    features = [[
        income,
        expenses,
        savings,
        goal_cost
    ]]

    prediction = model.predict(features)[0]

    probability = (
        model.predict_proba(features)[0][1]
        * 100
    )

    surplus = income - expenses

    remaining_amount = max(
        0,
        goal_cost - savings
    )

    required_daily_saving = (
        remaining_amount /
        max(target_days, 1)
    )

    required_weekly_saving = (
        required_daily_saving * 7
    )

    if surplus > 0:
        predicted_days = (
            remaining_amount / surplus
        ) * 30
    else:
        predicted_days = -1

    if income > 0:
        score = int(
            max(
                0,
                min(
                    100,
                    (surplus / income) * 100
                )
            )
        )
    else:
        score = 0

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💚 Health Score",
            f"{score}/100"
        )

    with col2:
        st.metric(
            "🎯 Success Chance",
            f"{probability:.1f}%"
        )

    with col3:
        if predicted_days >= 0:
            st.metric(
                "📅 Predicted Days",
                f"{predicted_days:.0f}"
            )
        else:
            st.metric(
                "📅 Predicted Days",
                "∞"
            )

    st.markdown("### 💰 Savings Plan")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Daily Target",
            f"₹{required_daily_saving:.0f}"
        )

    with col5:
        st.metric(
            "Weekly Target",
            f"₹{required_weekly_saving:.0f}"
        )

    with col6:
        st.metric(
            "Remaining Amount",
            f"₹{remaining_amount:,.0f}"
        )

    st.markdown("### 🎯 Goal Feasibility")

    monthly_required = required_daily_saving * 30

    if surplus >= monthly_required:
        st.success(
            f"✅ You can realistically achieve {goal_name} within {target_days} days."
        )
    else:
        st.error(
            f"❌ Based on your current finances, achieving {goal_name} within {target_days} days may be difficult."
        )

    st.markdown("### 📈 Dream Progress")

    progress = (
        savings /
        max(goal_cost, 1)
    ) * 100

    st.progress(
        min(
            int(progress),
            100
        )
    )

    st.write(
        f"Progress: {min(progress,100):.1f}%"
    )

    st.markdown("---")

    if prediction == 1:
        st.success(
            f"🎉 High probability of achieving {goal_name}"
        )
    else:
        st.error(
            f"⚠️ Achieving {goal_name} may be difficult right now"
        )

    st.markdown("### 🤖 AI Recommendation")

    st.info(
        f"""
Dream: {goal_name}

Target Time: {target_days} days

Predicted Time: {predicted_days:.0f} days

Daily Saving Needed: ₹{required_daily_saving:.0f}

Weekly Saving Needed: ₹{required_weekly_saving:.0f}

Remaining Amount: ₹{remaining_amount:,.0f}
"""
    )

    if probability >= 80:
        st.success(
            "Excellent financial position. Continue saving consistently."
        )
    elif probability >= 50:
        st.warning(
            "Moderate chance. Reducing expenses can help you reach your goal faster."
        )
    else:
        st.error(
            "Consider reducing expenses or increasing income."
        )

st.markdown("---")

st.caption(
    "💰 FinCheck AI | Machine Learning Powered Financial Goal Planner"
)
