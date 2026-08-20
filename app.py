from __future__ import annotations
from textwrap import dedent
import streamlit as st
from src.workout_planner import (EquipmentAccess, ExperienceLevel,
                                 FitnessGoal, WorkoutPreferences,
                                 generate_workout_plan,
                                 )
from src.utils import convert_to_docx


st.set_page_config(
    page_title="Workout Plan Generator",
    page_icon="🏋️",
    layout="wide",
)

# Custom CSS matching the header card style and increasing label sizes
st.markdown(
    """
    <style>
    /* Main Background */
    .stApp {
            background: linear-gradient(
                135deg,
                #00332c 0%,
                #004d40 35%,
                #26d0ce 60%,
                #20b2aa 100%
            );
            background-attachment: fixed;
    }

    /* Target all input labels (keys) to make them larger & crisp */
    .stSelectbox label,
    .stTextArea label {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 6px !important;
    }

    /* Form container matching the glassmorphism header card */
    [data-testid="stForm"] {
        background-color: rgba(0, 30, 25, 0.45) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.2) !important;
    }

    /* Style selectbox input field */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.12) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
    }

    /* Selectbox dropdown text & icons (collapsed state) */
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    /* Selectbox expanded dropdown menu container */
    div[data-baseweb="popover"] [data-baseweb="menu"] {
        background-color: #00332c !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }

    /* Dropdown options text color & hover states */
    div[data-baseweb="popover"] ul li {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    div[data-baseweb="popover"] ul li:hover,
    div[data-baseweb="popover"] ul li[aria-selected="true"] {
        background-color: #00695c !important;
        color: #80cbc4 !important;
    }

    /* Text Area custom matching glass styling */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.12) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 1.05rem !important;
    }

    .stTextArea textarea::placeholder {
        color: rgba(224, 242, 241, 0.6) !important;
    }

    /* Focus highlight for inputs */
    div[data-baseweb="select"]:focus-within > div,
    .stTextArea textarea:focus {
        border-color: #80cbc4 !important;
        box-shadow: 0 0 0 2px rgba(128, 203, 196, 0.3) !important;
    }

    /* Style form titles */
    [data-testid="stForm"] h3 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
    }

    /* Customizing primary form submit button */
    [data-testid="stForm"] button[type="submit"] {
        background-color: #00897b !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 0.5rem 1.8rem !important;
        transition: all 0.2s ease-in-out !important;
    }

    [data-testid="stForm"] button[type="submit"]:hover {
        background-color: #004d40 !important;
        border-color: #80cbc4 !important;
        transform: translateY(-1px);
    }

    /* Custom st.info Alert Styling */
    div[data-testid="stAlert"] {
        background-color: rgba(0, 30, 25, 0.55) !important;
        border: 1px solid rgba(128, 203, 196, 0.4) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
    }

    /* Info Alert Text Color */
    div[data-testid="stAlert"] * {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }

    /* Info Icon Color */
    div[data-testid="stAlert"] svg {
        fill: #80cbc4 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Your Personalized Workout Plan")
st.subheader("Generated in seconds")
st.caption("Personalized for your goals, experience, equipment and limitations")

# Header card
st.markdown(
    dedent(
        """
        <div style="
            background-color: rgba(0, 30, 25, 0.45);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.2);
        ">
            <strong style="color: #ffffff; font-size: 1.25em; letter-spacing: 0.5px;">How it works</strong><br>
            <span style="color: #e0f2f1; line-height: 1.6; display: block; margin-top: 6px; font-size: 1.05rem;">
                Pick a goal, experience level, training frequency, and equipment access. The app generates the customized plan.
            </span>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

# Initialize Session State
if "last_plan" not in st.session_state:
    st.session_state.last_plan = ""
if "last_error" not in st.session_state:
    st.session_state.last_error = ""

# Form with side-by-side inputs
with st.form("user_input_form"):
    st.subheader("Let us know your preferences")

    # First row of inputs
    col1, col2 = st.columns(2)
    with col1:
        height: int = st.number_input(
            "Height (cm)",
            value=160,
            min_value=100,
            max_value=250
        )
    with col2:
        weight: int = st.number_input(
            "Weight (kg)",
            value=60,
            min_value=30,
            max_value=200
        )

    # Second row of inputs
    col3, col4 = st.columns(2)
    with col3:
        fitness_goal: FitnessGoal = st.selectbox(
            "Fitness goal",
            ["Build muscle", "Lose fat", "General fitness", "Improve endurance"],
        )
    with col4:
        experience_level: ExperienceLevel = st.selectbox(
            "Experience level",
            ["Beginner", "Intermediate", "Advanced"],
        )

    # Third row of inputs
    col5, col6 = st.columns(2)
    with col5:

        days_per_week: int = st.selectbox(
            "Days available per week",
            [1, 2, 3, 4, 5, 6, 7],
        )

    with col6:
        mins_per_day: int = st.number_input(
                    "Minutes available per day",
                    value=30,
                    min_value=15,
                    max_value=200
                )

    # Fourth row of inputs
    col7, col8 = st.columns(2)
    with col7:
        equipment_access: EquipmentAccess = st.selectbox(
                    "Equipment access",
                    ["No equipment", "Home dumbbells", "Full gym"],
                )

    with col8:
        goal_weight: int = st.number_input(
            "Goal weight (kg)",
            value=60,
            min_value=40,
            max_value=200
        )

    # Text area for limitations
    injuries_or_limitations = st.text_area(
        "Injuries or limitations (optional)",
        placeholder="For example: bad knees, no overhead pressing, lower back sensitivity",
        height=80,
    )

    # Dynamic button label
    button_label = "Regenerate Plan" if st.session_state.last_plan else "Generate Plan"

    # Centering the submit button using a 3-column layout
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        generate_clicked = st.form_submit_button(
            button_label,
            type="primary",
            use_container_width=True
        )

# Form processing logic
if generate_clicked:
    if days_per_week < 1:
        st.session_state.last_error = "Please choose at least 1 training day."
        st.session_state.last_plan = ""
    else:
        preferences = WorkoutPreferences(
            height=height,
            weight=weight,
            fitness_goal=fitness_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            mins_per_day=mins_per_day,
            equipment_access=equipment_access,
            goal_weight=goal_weight,
            injuries_or_limitations=injuries_or_limitations,
        )
        print(f"Generating workout plan with preferences: {preferences}")
        with st.spinner("Building your workout plan..."):
            try:
                plan = generate_workout_plan(preferences)
                st.session_state.last_plan = plan
                st.session_state.last_error = ""
            except Exception as exc:  # noqa: BLE001 - user-facing error handling
                st.session_state.last_error = str(exc)
                st.session_state.last_plan = ""

# Output section rendered below the form
st.write("---")
st.subheader("Generated plan")

if st.session_state.last_error:
    st.error(st.session_state.last_error)
    st.info(
        "Set `GROQ_API_KEY` in your environment or `.env` file, then click Generate Plan again."
    )
elif st.session_state.last_plan:
    with st.container(border=True):
        st.markdown(st.session_state.last_plan)

    # Generate docx bytes
    docx_data = convert_to_docx(st.session_state.last_plan)

    # Download button
    st.download_button(
        "Download plan as document",
        data=docx_data,
        file_name="workout-plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=False,
    )
else:
    st.info("Your personalized plan will appear here after you click generate.")
