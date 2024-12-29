import pandas as pd
import streamlit as st

# Load data
def load_data(uploaded_file):
    try:
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()  # Strip whitespace from column names
        return data
    except Exception as e:
        st.error(f"Error loading the data: {e}")
        return None

# Preprocess data
def preprocess_data(data):
    data.fillna(0, inplace=True)

    # Ensure numeric columns and handle missing ones
    numeric_columns = [
        'GPA', 'Hackathons', 'Projects', 'Papers',
        'Teacher Assistance', 'Core Engineering Score',
        'Consistency', 'Extracurriculars', 'Internships', 'Leadership Roles'
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        else:
            data[column] = 0

    # Handle Attendance column
    if 'Attendance' in data.columns:
        data['Attendance'] = data['Attendance'].str.rstrip('%').astype(float)

    return data

# Filter students based on attendance
def filter_students(data, filter_option):
    if 'Attendance' not in data.columns:
        st.error("Attendance column is missing in the dataset.")
        return None

    threshold_low = 65  # Minimum attendance percentage for detained students
    threshold_high = 75  # Minimum attendance percentage for condonation

    if filter_option == "Detained Students":
        return data[data['Attendance'] < threshold_low]
    elif filter_option == "Condonation Students":
        return data[(data['Attendance'] >= threshold_low) & (data['Attendance'] < threshold_high)]
    elif filter_option == "All Students' Attendance":
        return data
    else:
        return data

# Highlight rows based on attendance
def highlight_rows(row):
    if row['Attendance'] < 65:
        return ['background-color: #f97b98'] * len(row)
    elif 65 <= row['Attendance'] < 75:
        return ['background-color: #576ed1'] * len(row)
    return [''] * len(row)

# Main Streamlit app
def main():
    

    uploaded_file = st.file_uploader("Upload student dataset (CSV file)", type="csv")
    st.title("Attendance Management System")

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        if data is not None:
            st.write("Dataset Preview:")
            st.write(data.head(5))

            data_preprocessed = preprocess_data(data)

            filter_option = st.selectbox("Select filter for attendance:", ["All Students", "Detained Students", "Condonation Students"])

            filtered_data = filter_students(data_preprocessed, filter_option)

            if filtered_data is not None:
                st.dataframe(filtered_data[['StudentID', 'Name', 'Attendance']].style.apply(highlight_rows, axis=1), use_container_width=True)

        # Link custom CSS
        st.markdown("<style>{}</style>".format(open("assets/styles.css").read()), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
