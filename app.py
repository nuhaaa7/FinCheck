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

    if surplus > 0:

        days_needed = (
            remaining_amount / surplus
        ) * 30

        daily_saving_needed = (
            remaining_amount /
            max(days_needed, 1)
        )

        weekly_saving_needed = (
            daily_saving_needed * 7
        )

    else:

        days_needed = -1
        daily_saving_needed = 0
        weekly_saving_needed = 0

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

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "💚 Health Score",
            f"{score}/100"
        )

    with c2:
        st.metric(
            "🎯 Success Chance",
            f"{probability:.1f}%"
        )

    with c3:
        if days_needed >= 0:
            st.metric(
                "📅 Days Needed",
                f"{days_needed:.0f}"
            )
        else:
            st.metric(
                "📅 Days Needed",
                "∞"
            )

    st.markdown("### 💰 Savings Plan")

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric(
            "Daily Target",
            f"₹{daily_saving_needed:.0f}"
        )

    with c5:
        st.metric(
            "Weekly Target",
            f"₹{weekly_saving_needed:.0f}"
        )

    with c6:
        st.metric(
            "Remaining Amount",
            f"₹{remaining_amount:,.0f}"
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
To achieve {goal_name}:

• Save approximately ₹{daily_saving_needed:.0f} per day

• Save approximately ₹{weekly_saving_needed:.0f} per week

• Remaining amount needed: ₹{remaining_amount:,.0f}

• Estimated completion time: {days_needed:.0f} days
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
