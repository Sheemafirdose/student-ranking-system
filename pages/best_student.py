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

    # Calculate the overall score if not already present
    if 'Overall Score' not in data.columns:
        data['Overall Score'] = (
            data['GPA'] * 0.7 +
            data['Hackathons'] * 0.2 +
            data['Projects'] * 0.1 +
            data['Teacher Assistance'] * 0.05 +
            data['Core Engineering Score'] * 0.1 +
            data['Consistency'] * 0.05 +
            data['Extracurriculars'] * 0.025 +
            data['Internships'] * 0.025 +
            data['Leadership Roles'] * 0.05
        )

    # Normalize the Overall Score
    min_score = 6
    max_score = 9.6
    highest_score = data['Overall Score'].max()
    data['ScaledOverallScore'] = ((data['Overall Score'] - data['Overall Score'].min()) / 
                                  (highest_score - data['Overall Score'].min())) * (max_score - min_score) + min_score

    return data

# Rank students
def rank_students(data):
    data_sorted = data.sort_values(by='ScaledOverallScore', ascending=False).reset_index(drop=True)
    data_sorted['Rank'] = range(1, len(data_sorted) + 1)
    data_sorted['FormattedScore'] = data_sorted['ScaledOverallScore'].round(2)
    return data_sorted

# Main Streamlit app
def main():
    
    uploaded_file = st.file_uploader("Upload student dataset (CSV file)", type="csv")
    st.title("Best-Performing Student Recognition System")

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        if data is not None:
            

            data_preprocessed = preprocess_data(data)
            data_ranked = rank_students(data_preprocessed)
            st.write("Dataset Preview:")
            st.write(data.head(5))

            st.subheader("Query a Student's Details:")
            query_id = st.text_input("Enter Student ID:")
            submit_button = st.button("Check Student Details")

            if submit_button:
                if query_id:
                    student = data_ranked[data_ranked['StudentID'].astype(str) == query_id]
                    if not student.empty:
                        st.subheader(f"Details for Student ID {query_id}:")
                        student_details = student.iloc[0]
                        if 'Attendance' in student_details:
                            st.table(pd.DataFrame([
                                ['Name', student_details['Name']],
                                ['Branch', student_details['Branch']],
                                ['Rank', student_details['Rank']],
                                ['Overall Score', f"{student_details['FormattedScore']:.2f}"],
                                ['GPA', f"{student_details['GPA']:.2f}" if student_details['GPA'] != 0 else 'Not Provided'],
                                ['Hackathons', student_details['Hackathons']],
                                ['Projects', student_details['Projects']],
                                ['Internships', student_details['Internships']],
                                ['Attendance', student_details['Attendance']]  # Including Attendance
                            ], columns=['Attribute', 'Value']))
                        else:
                            st.table(pd.DataFrame([
                                ['Name', student_details['Name']],
                                ['Branch', student_details['Branch']],
                                ['Rank', student_details['Rank']],
                                ['Overall Score', f"{student_details['FormattedScore']:.2f}"],
                                ['GPA', f"{student_details['GPA']:.2f}" if student_details['GPA'] != 0 else 'Not Provided'],
                                ['Hackathons', student_details['Hackathons']],
                                ['Projects', student_details['Projects']],
                                ['Internships', student_details['Internships']]
                            ], columns=['Attribute', 'Value']))
                    else:
                        st.error("Student not found. Please check the Student ID.")
            st.subheader("Top Performing Students:")

            # Dropdown menu to select the number of students to display
            num_students = st.selectbox("Select the number of top students to display:", [3, 10, 30, 50])

            # Display the top N students including the Attendance column only if available
            if 'Attendance' in data_ranked.columns:
                st.table(data_ranked[['Rank', 'StudentID', 'Name', 'FormattedScore', 'Attendance']].head(num_students))
            else:
                st.table(data_ranked[['Rank', 'StudentID', 'Name', 'FormattedScore']].head(num_students))
            

if __name__ == "__main__":
    main()
