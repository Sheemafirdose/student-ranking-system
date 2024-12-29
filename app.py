import streamlit as st
from streamlit_option_menu import option_menu


# Custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title and Welcome Message
st.title("Student Management System")
st.subheader("Welcome to the Student Portal!")

st.write("Choose an option below to proceed:")

# Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["Results", "Attendance"],
    icons=["trophy", "clipboard"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#ffffff"},  # White background
        "icon": {"color": "blue", "font-size": "25px"},  # Keeping blue color but modifying font size
        "nav-link": {
            "font-size": "20px",
            "text-align": "center",
            "margin": "0px",
            "color": "black",  # Text color set to black
            "--hover-color": "#f0f0f0",  # Light grey hover color
        },
        "nav-link-selected": {"background-color": "#008cba"},  # A more vibrant blue for selected links
    }
)

if selected == "Results":
    # Execute Best_Student_Recognition.py
    exec(open("pages/Best_Student.py").read())
elif selected == "Attendance":
    # Execute Attendance.py
    exec(open("pages/Attendance.py").read())