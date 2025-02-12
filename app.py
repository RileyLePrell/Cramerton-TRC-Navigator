import streamlit as st
from datetime import datetime, timedelta

# Set Streamlit page config
st.set_page_config(page_title="Cramerton TRC Navigator", layout="wide")

# 🎨 Custom CSS for Sidebar & Styling
st.markdown(
    """
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0D6051 !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: white !important;
        }
        
        /* Main Page Styling */
        .main-container {
            background-color: #f0f2e9;
            padding: 20px;
            border-radius: 10px;
        }

        /* Box Styling */
        .timeline-box {
            background: white;
            border-radius: 8px;
            padding: 10px;
            text-align: left;
            font-size: 16px;
            font-weight: bold;
            margin: 10px auto;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            width: 300px;
            position: relative;
        }

        .timeline-box p {
            margin: 5px 0;
        }

        /* Center the Timeline Title */
        .timeline-header {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #0D6051;
            margin-top: 20px;
        }

        /* Center Align Flowchart */
        .flowchart-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Info Icon Styling */
        .info-icon {
            font-size: 16px;
            font-weight: bold;
            color: #0D6051;
            cursor: help;
            position: absolute;
            top: 10px;
            right: 10px;
        }
    </style>
    """, unsafe_allow_html=True
)

# ⏪ Sidebar - Welcome Message & Inputs
st.sidebar.title("Welcome to the TRC Review Process Timeline Application")
st.sidebar.markdown(
    "This application helps applicants track their submissions through the **Technical Review Committee (TRC) Process** "
    "for **Rezonings, Preliminary Plats, Construction Drawings, and Final Plats.** "
    "Simply **select your submission type** and **submission date**, and this tool will generate your review timeline."
)

submission_type = st.sidebar.selectbox(
    "Select Submission Type", 
    ["", "Rezoning (Conditional)", "Rezoning (General)", "Preliminary Plat", "Construction Drawings", "Final Plat"]
)

submission_date = st.sidebar.date_input("Select Submission Date", None)  # No default date

# Function to determine the first Monday of the next available month
def get_first_monday(date):
    first_day_next_month = (date.replace(day=1) + timedelta(days=31)).replace(day=1)
    while first_day_next_month.weekday() != 0:  # 0 = Monday
        first_day_next_month += timedelta(days=1)
    return first_day_next_month

# Function to determine required submission documents
def get_required_documents(submission_type):
    documents = {
        "Rezoning (Conditional)": "📌 **You Need:** Rezoning Application, Rezoning Fee, Rezoning Sketch Plan.",
        "Rezoning (General)": "📌 **You Need:** Rezoning Application, Rezoning Fee, Rezoning Sketch Plan.",
        "Preliminary Plat": "📌 **You Need:** Preliminary Plat, Preliminary Plat Fee.",
        "Construction Drawings": "📌 **You Need:** Construction Drawings.",
        "Final Plat": "📌 **You Need:** Final Plat Fee, Final Plat, Subdivision Bond Estimate."
    }
    return documents.get(submission_type, "")

# Function to calculate timeline only if both type & date are selected
def calculate_timeline(submission_type, submission_date):
    if not submission_type or submission_date is None:
        return []

    timeline = []

    # Pre-Application Meeting is 7 days before the **selected submission date**
    if "Rezoning" in submission_type:
        pre_app_meeting = submission_date - timedelta(days=7)
        timeline.append(("Pre-Application Meeting", pre_app_meeting, 
                         "🧑‍💼 Must be held before submission.",
                         "To set up a meeting, contact rleprell@cramerton.org or jwatkins@cramerton.org"))

    first_monday = get_first_monday(submission_date)

    timeline.append(("Application Submission", first_monday, 
        "📌 Needs to be submitted by this date.",
        get_required_documents(submission_type)))

    plan_distribution = first_monday + timedelta(days=1)
    timeline.append(("Plans Sent to TRC", plan_distribution, "📤 Plans sent for review.", None))

    first_tuesday = get_first_monday(plan_distribution)
    while first_tuesday.weekday() != 1:  # 1 = Tuesday
        first_tuesday += timedelta(days=1)
    
    timeline.append(("TRC Meeting", first_tuesday, "📅 Committee review meeting.", None))

    comments_return = first_tuesday + timedelta(days=2)
    resubmission_date = get_first_monday(comments_return)
    timeline.append(("Comments Returned", comments_return, 
        f"📝 Feedback provided. Resubmit if needed by {resubmission_date.strftime('%B %d, %Y')}.",
        None))

    # If rezoning, include Planning Board & BOC steps
    if "Rezoning" in submission_type:
        first_thursday = get_first_monday(comments_return)
        while first_thursday.weekday() != 3:  # 3 = Thursday
            first_thursday += timedelta(days=1)

        timeline.append(("Planning Board Meeting", first_thursday, "📊 Planning Board review.", None))

        third_tuesday = first_thursday.replace(day=1)
        while third_tuesday.weekday() != 1:  # 1 = Tuesday
            third_tuesday += timedelta(days=1)
        
        third_tuesday += timedelta(weeks=2)
        timeline.append(("Board of Commissioners (BOC) Hearing", third_tuesday, "🏛 Final approval process.", None))

    return timeline

# Only show the timeline if BOTH submission type & date are selected
if not submission_type or submission_date is None:
    st.markdown(
        "<div style='text-align: center; padding: 20px; font-size: 18px; color: #0D6051; background-color: #f0f2e9; "
        "border-radius: 10px;'>🛠 Select **Submission Type** and **Submission Date** in Sidebar to Populate Timeline</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown("<div class='timeline-header'>Technical Review Committee Timeline Scenario</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='flowchart-container'>", unsafe_allow_html=True)

    for step, date, description, hover_info in calculate_timeline(submission_type, submission_date):
        info_icon = f"<span class='info-icon' title='{hover_info}'>ℹ️</span>" if hover_info else ""
        st.markdown(f"""
        <div class="timeline-box">
            <p>{date.strftime('%B %d, %Y')}</p>
            <p><strong>{step} {info_icon}</strong></p>
            <p style="font-size: 14px;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
