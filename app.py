import streamlit as st
from ai_analyzer import generate_study_plan

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for "Antigravity" vibe
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stTextInput input, .stNumberInput input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 10px;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.2);
    }
    .stButton button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        color: white;
    }
    h1 {
        color: #0f172a;
        font-family: 'Inter', sans-serif;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .response-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 20px;
        border-left: 5px solid #8b5cf6;
    }
    .st-emotion-cache-1v0mbdj > img {
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧠 AI Study Planner")
st.markdown("<p class='subtitle'>Your personalized roadmap to academic success. 🚀</p>", unsafe_allow_html=True)

st.write("### Tell me about your exam!")

col1, col2 = st.columns(2)

with col1:
    subjects = st.text_input("List of subjects (comma separated)", placeholder="e.g. Math, Physics, Chemistry")
    study_hours = st.number_input("Study hours available per day", min_value=0.5, max_value=24.0, value=4.0, step=0.5)

with col2:
    days_left = st.number_input("Number of days left for exam", min_value=1, max_value=365, value=30, step=1)
    weak_subject = st.text_input("Weak subject (optional)", placeholder="e.g. Physics")

if st.button("Generate Study Plan 📅"):
    if not subjects.strip():
        st.warning("Please provide at least one subject to study! 📝")
    else:
        with st.spinner("Analyzing subjects and optimizing your schedule... ⏳"):
            # Call AI analyzer
            result = generate_study_plan(subjects, days_left, study_hours, weak_subject)
            
            # Display results
            st.markdown("<div class='response-card'>", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("</div>", unsafe_allow_html=True)
            
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.9rem;'>Powered by Antigravity Magic & Gemini AI ✨</p>", unsafe_allow_html=True)
