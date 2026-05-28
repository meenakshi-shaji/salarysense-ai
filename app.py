import streamlit as st
import pandas as pd
import joblib
import pdfplumber
import plotly.express as px
import os
import nltk

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from database import (
    add_user,
    login_user,
    save_prediction,
    get_predictions,
    update_username,
    update_password
)

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="SalarySense AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# LOAD MODEL + ENCODERS
# =========================================

model = joblib.load("model.pkl")

job_encoder = joblib.load(
    "job_encoder.pkl"
)

location_encoder = joblib.load(
    "location_encoder.pkl"
)

industry_encoder = joblib.load(
    "industry_encoder.pkl"
)

# =========================================
# LOAD DATASET
# =========================================

data = pd.read_csv(
    "dataset/job_salary_prediction_dataset.csv"
)

# =========================================
# SESSION STATE
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================
# UI DESIGN
# =========================================

st.markdown(
    """
    <style>

    .stApp{
        background-color:#050505;
        color:white;
    }

    section[data-testid="stSidebar"]{
        background-color:#0d0d0d;
        border-right:1px solid #222;
    }

    h1,h2,h3,h4,h5,h6,p,label,span{
        color:white !important;
    }

    .stButton > button{

        background:linear-gradient(
            135deg,
            #7c3aed,
            #2563eb
        );

        color:white;

        border:none;

        border-radius:14px;

        height:50px;

        font-size:16px;

        font-weight:600;
    }

    .stTextInput input,
    .stSelectbox div,
    .stTextArea textarea{

        background-color:#111111 !important;

        color:white !important;

        border:1px solid #2a2a2a !important;

        border-radius:12px !important;
    }

    .glass{

        background:rgba(255,255,255,0.04);

        border:1px solid rgba(
            255,
            255,
            255,
            0.08
        );

        border-radius:24px;

        padding:30px;

        backdrop-filter:blur(16px);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# PDF FUNCTION
# =========================================

def create_salary_pdf(
    username,
    role,
    location,
    industry,
    experience,
    skills,
    salary
):

    file_name = "salary_report.pdf"

    c = canvas.Canvas(
        file_name,
        pagesize=letter
    )

    c.setFont(
        "Helvetica-Bold",
        24
    )

    c.drawString(
        150,
        750,
        "SalarySense AI"
    )

    c.setFont(
        "Helvetica",
        16
    )

    c.drawString(
        50,
        680,
        f"Username: {username}"
    )

    c.drawString(
        50,
        650,
        f"Job Role: {role}"
    )

    c.drawString(
        50,
        620,
        f"Location: {location}"
    )

    c.drawString(
        50,
        590,
        f"Industry: {industry}"
    )

    c.drawString(
        50,
        560,
        f"Experience: {experience} Years"
    )

    c.drawString(
        50,
        530,
        f"Skills Count: {skills}"
    )

    c.drawString(
        50,
        500,
        f"Predicted Salary: {salary}"
    )

    c.save()

    return file_name

# =========================================
# LOGIN PAGE
# =========================================

if st.session_state.logged_in == False:

    st.markdown(
        """
        <div style='text-align:center;'>

        <h1 style='
        font-size:90px;
        font-weight:800;
        '>

        SalarySense AI

        </h1>

        <p style='
        font-size:24px;
        color:gray;
        '>

        AI-powered career intelligence platform

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Create Account"
        ]
    )

    # =====================================
    # LOGIN
    # =====================================

    with tab1:

        st.markdown(
            """
            <div class="glass">
            <h2>Login</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Continue"
        ):

            result = login_user(
                username,
                password
            )

            if result:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    # =====================================
    # CREATE ACCOUNT
    # =====================================

    with tab2:

        st.markdown(
            """
            <div class="glass">
            <h2>Create Account</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        new_user = st.text_input(
            "Create Username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button(
            "Create Account"
        ):

            add_user(
                new_user,
                new_password
            )

            st.success(
                "Account Created Successfully"
            )

# =========================================
# MAIN APP
# =========================================

else:

    st.sidebar.title(
        "Dashboard"
    )

    page = st.sidebar.radio(
        "Go To",
        [
            "Home",
            "Salary Predictor",
            "Resume Analyzer",
            "Career Insights",
            "Prediction History",
            "Downloads",
            "My Account",
            "Settings",
            "Admin Dashboard"
        ]
    )

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()

    # =====================================
    # HOME
    # =====================================

    if page == "Home":

        st.markdown(
            """
            <div class="glass">

            <h1 style="
            font-size:60px;
            font-weight:800;
            ">

            Welcome to SalarySense AI

            </h1>

            <p style="
            font-size:22px;
            color:gray;
            line-height:1.8;
            ">

            Predict salaries using AI,
            analyze resumes,
            improve ATS scores,
            and explore career growth
            with intelligent analytics.

            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================
    # SALARY PREDICTOR
    # =====================================

    elif page == "Salary Predictor":

        st.header(
            "Salary Predictor"
        )

        job_roles = sorted(
            data["job_title"].unique()
        )

        locations = sorted(
            data["location"].unique()
        )

        industries = sorted(
            data["industry"].unique()
        )

        col1, col2 = st.columns(2)

        with col1:

            role = st.selectbox(
                "Select Job Role",
                ["Select"] + job_roles
            )

            location = st.selectbox(
                "Select Location",
                ["Select"] + locations
            )

            industry = st.selectbox(
                "Select Industry",
                ["Select"] + industries
            )

            company_size = st.selectbox(
                "Company Size",
                [
                    "Select",
                    "Small",
                    "Medium",
                    "Large"
                ]
            )

        with col2:

            experience = st.slider(
                "Experience Years",
                0,
                20
            )

            skills = st.slider(
                "Skills Count",
                1,
                20
            )

            certifications = st.slider(
                "Certifications",
                0,
                15
            )

            remote_work = st.selectbox(
                "Remote Work",
                [
                    "Hybrid",
                    "Remote",
                    "Onsite"
                ]
            )

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        predict_button = st.button(
            "Predict Salary"
        )

        if predict_button:

            if (
                role == "Select"
                or location == "Select"
                or industry == "Select"
                or company_size == "Select"
            ):

                st.error(
                    "Please select all required fields."
                )

            else:

                role_encoded = job_encoder.transform(
                    [role]
                )[0]

                location_encoded = location_encoder.transform(
                    [location]
                )[0]

                industry_encoded = industry_encoder.transform(
                    [industry]
                )[0]

                prediction = model.predict(
                    [[
                        role_encoded,
                        location_encoded,
                        industry_encoded,
                        experience,
                        skills
                    ]]
                )[0]

                salary_lpa = prediction / 100000

                # =====================================
                # INDUSTRY STANDARD BASE SALARIES
                # =====================================

                base_salary = {

                    "AI Engineer": 8,
                    "Machine Learning Engineer": 9,
                    "Data Scientist": 7.5,
                    "Data Analyst": 5,
                    "Software Engineer": 6,
                    "Backend Developer": 6.5,
                    "Frontend Developer": 5.5,
                    "Full Stack Developer": 7,
                    "Cloud Engineer": 8,
                    "Cybersecurity Analyst": 7,
                    "DevOps Engineer": 8,
                    "Business Analyst": 5,
                    "Product Manager": 10,
                    "Mobile App Developer": 6,
                    "Web Developer": 5,
                    "Database Administrator": 6,
                    "UI/UX Designer": 5,
                    "Network Engineer": 5.5,
                    "Systems Engineer": 6,
                    "Blockchain Developer": 10
                }

                if role in base_salary:

                    salary_lpa = base_salary[role]

                else:

                    salary_lpa = 4.5

                # =====================================
                # EXPERIENCE BOOST
                # =====================================

                if experience <= 1:

                    salary_lpa += 0.5

                elif experience <= 3:

                    salary_lpa += 2

                elif experience <= 5:

                    salary_lpa += 4

                elif experience <= 8:

                    salary_lpa += 7

                else:

                    salary_lpa += 10

                # =====================================
                # SKILLS BOOST
                # =====================================

                salary_lpa += skills * 0.25

                # =====================================
                # CERTIFICATION BOOST
                # =====================================

                salary_lpa += certifications * 0.3

                # =====================================
                # COMPANY SIZE BOOST
                # =====================================

                if company_size == "Medium":

                    salary_lpa += 1.5

                elif company_size == "Large":

                    salary_lpa += 3

                # =====================================
                # LOCATION BOOST
                # =====================================

                high_salary_locations = [

                    "USA",
                    "Canada",
                    "Germany",
                    "Australia",
                    "Singapore",
                    "United Kingdom"

                ]

                mid_salary_locations = [

                    "India",
                    "UAE",
                    "Malaysia"

                ]

                if location in high_salary_locations:

                    salary_lpa += 6

                elif location in mid_salary_locations:

                    salary_lpa += 2

                # =====================================
                # INDUSTRY BOOST
                # =====================================

                high_paying_industries = [

                    "Finance",
                    "AI",
                    "Cloud Computing",
                    "Cybersecurity",
                    "Technology"

                ]

                if industry in high_paying_industries:

                    salary_lpa += 3

                # =====================================
                # REMOTE WORK BOOST
                # =====================================

                if remote_work == "Remote":

                    salary_lpa += 1.5

                elif remote_work == "Hybrid":

                    salary_lpa += 0.5

                # =====================================
                # FINAL ROUNDING
                # =====================================

                salary_lpa = round(
                    salary_lpa,
                    2
                )

                # =====================================
                # RESULT UI
                # =====================================

                st.success(
                    f"Predicted Salary: ₹{salary_lpa:.2f} LPA"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Estimated Salary",
                        f"₹{salary_lpa:.2f} LPA"
                    )

                with col2:

                    if salary_lpa < 6:

                        level = "Beginner"

                    elif salary_lpa < 12:

                        level = "Professional"

                    else:

                        level = "High Demand"

                    st.metric(
                        "Career Level",
                        level
                    )

                with col3:

                    growth = (
                        10
                        + certifications
                        + skills
                    )

                    st.metric(
                        "Growth Potential",
                        f"{growth}%"
                    )

                save_prediction(
                    st.session_state.username,
                    role,
                    location,
                    experience,
                    f"₹{salary_lpa:.2f} LPA"
                )

                pdf_file = create_salary_pdf(
                    st.session_state.username,
                    role,
                    location,
                    industry,
                    experience,
                    skills,
                    f"₹{salary_lpa:.2f} LPA"
                )

                with open(
                    pdf_file,
                    "rb"
                ) as file:

                    st.download_button(
                        label="Download Salary Report",
                        data=file,
                        file_name="salary_report.pdf",
                        mime="application/pdf"
                    )

                st.info(
                    "Recommendation: Increase certifications, skills, and experience to improve salary growth."
                )

    # =====================================
    # RESUME ANALYZER
    # =====================================

    elif page == "Resume Analyzer":

        st.header(
            "Resume Analyzer"
        )

        uploaded_file = st.file_uploader(
            "Upload Resume PDF",
            type=["pdf"]
        )

        if uploaded_file is not None:

            resume_text = ""

            with pdfplumber.open(
                uploaded_file
            ) as pdf:

                for page_pdf in pdf.pages:

                    text = page_pdf.extract_text()

                    if text:
                        resume_text += text

            st.subheader(
                "Resume Content"
            )

            st.text_area(
                "Extracted Resume Text",
                resume_text,
                height=250
            )

            resume_lower = resume_text.lower()

            technical_skills = [

                "python",
                "sql",
                "machine learning",
                "data science",
                "deep learning",
                "excel",
                "power bi",
                "tableau",
                "tensorflow",
                "pandas",
                "numpy",
                "java",
                "c++",
                "streamlit",
                "flask",
                "django",
                "html",
                "css",
                "javascript",
                "react",
                "communication",
                "leadership"

            ]

            found_skills = []
            missing_skills = []

            for skill in technical_skills:

                if skill in resume_lower:
                    found_skills.append(skill)

                else:
                    missing_skills.append(skill)

            ats_score = int(
                (
                    len(found_skills)
                    / len(technical_skills)
                ) * 100
            )

            st.subheader(
                "ATS Score"
            )

            st.progress(
                ats_score
            )

            st.success(
                f"Your ATS Score: {ats_score}%"
            )

            if ats_score >= 80:
                strength = "Excellent Resume"

            elif ats_score >= 60:
                strength = "Good Resume"

            elif ats_score >= 40:
                strength = "Average Resume"

            else:
                strength = "Needs Improvement"

            st.info(
                f"Resume Strength: {strength}"
            )

            st.subheader(
                "Detected Skills"
            )

            for skill in found_skills:
                st.success(skill)

            st.subheader(
                "Recommended Skills"
            )

            for skill in missing_skills[:8]:
                st.warning(skill)

    # =====================================
    # CAREER INSIGHTS
    # =====================================

    elif page == "Career Insights":

        st.header(
            "Career Insights"
        )

        chart = px.histogram(
            data,
            x="industry",
            title="Industry Distribution"
        )

        chart.update_layout(
            paper_bgcolor="#111111",
            plot_bgcolor="#111111",
            font_color="white"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    # =====================================
    # PREDICTION HISTORY
    # =====================================

    elif page == "Prediction History":

        st.header(
            "Prediction History"
        )

        history = get_predictions(
            st.session_state.username
        )

        if len(history) == 0:

            st.warning(
                "No prediction history found"
            )

        else:

            history_df = pd.DataFrame(
                history,
                columns=[
                    "Job Role",
                    "Location",
                    "Experience",
                    "Salary"
                ]
            )

            st.dataframe(
                history_df,
                use_container_width=True
            )

    # =====================================
    # DOWNLOADS
    # =====================================

    elif page == "Downloads":

        st.header(
            "Downloads"
        )

        if os.path.exists(
            "salary_report.pdf"
        ):

            with open(
                "salary_report.pdf",
                "rb"
            ) as file:

                st.download_button(
                    "Download Salary PDF",
                    data=file,
                    file_name="salary_report.pdf",
                    mime="application/pdf"
                )

    # =====================================
    # MY ACCOUNT
    # =====================================

    elif page == "My Account":

        st.header(
            "My Account"
        )

        st.subheader(
            st.session_state.username
        )

        new_username = st.text_input(
            "New Username"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button(
            "Save Changes"
        ):

            if new_username != "":

                update_username(
                    st.session_state.username,
                    new_username
                )

                st.session_state.username = new_username

            if new_password != "":

                update_password(
                    st.session_state.username,
                    new_password
                )

            st.success(
                "Profile Updated Successfully"
            )

    # =====================================
    # SETTINGS
    # =====================================

    elif page == "Settings":

        st.header(
            "Settings"
        )

        st.toggle(
            "Enable Notifications"
        )

        st.toggle(
            "Auto Save Reports"
        )

    # =====================================
    # ADMIN DASHBOARD
    # =====================================

    elif page == "Admin Dashboard":

        st.header(
            "Admin Dashboard"
        )

        st.metric(
            "Total Job Roles",
            len(
                data["job_title"].unique()
            )
        )

        admin_chart = px.histogram(
            data,
            x="location",
            title="Top Locations"
        )

        admin_chart.update_layout(
            paper_bgcolor="#111111",
            plot_bgcolor="#111111",
            font_color="white"
        )

        st.plotly_chart(
            admin_chart,
            use_container_width=True
        )