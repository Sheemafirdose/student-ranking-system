
import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler  # Correct import


# Load data
def load_data(uploaded_file):
    """Load the dataset uploaded by the user."""
    try:
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()  # Strip whitespace from column names
        return data
    except Exception as e:
        st.error(f"Error loading the data: {e}")
        return None

# Preprocess data
def preprocess_data(data):
    """
    Preprocess the data: fill missing values, normalize columns,
    and calculate overall score.
    """
    # Fill missing values with 0
    data.fillna(0, inplace=True)

    # Define all possible numeric columns for ranking, including both GPA and other columns
    all_columns = [
        'GPA', 'Hackathons', 'Projects', 'Papers',
        'Teacher Assistance', 'Core Engineering Score',
        'Consistency', 'Extracurriculars', 'Internships', 'Leadership Roles'
    ]

    # Ensure numeric columns are in dataset and handle missing ones
    for column in all_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        else:
            data[column] = 0  # Add missing columns with default value 0

    # Normalize available columns
    numeric_columns = [col for col in all_columns if col != 'Papers']  # Exclude 'Papers' from normalization
    scaler = MinMaxScaler()
    data_normalized = pd.DataFrame(
        scaler.fit_transform(data[numeric_columns]),
        columns=numeric_columns
    )

    # Calculate Overall Score
    data['OverallScore'] = (
        data_normalized['GPA'] * 0.7 +
        data_normalized['Hackathons'] * 0.2 +
        data_normalized['Projects'] * 0.1 +
        data_normalized['Teacher Assistance'] * 0.05 +
        data_normalized['Core Engineering Score'] * 0.1 +
        data_normalized['Consistency'] * 0.05 +
        data_normalized['Extracurriculars'] * 0.025 +
        data_normalized['Internships'] * 0.025 +
        data_normalized['Leadership Roles'] * 0.05
    )

    # Normalize OverallScore to range from 6 to 10
    min_score = 6
    max_score = 9.8
    highest_score = data['OverallScore'].max()
    data['ScaledOverallScore'] = ((data['OverallScore'] - data['OverallScore'].min()) /
                                  (highest_score - data['OverallScore'].min())) * (max_score - min_score) + min_score

    return data

# Rank students
def rank_students(data):
    """Rank the students based on their ScaledOverallScore."""
    # Sort data by ScaledOverallScore descending
    data_sorted = data.sort_values(by='ScaledOverallScore', ascending=False).reset_index(drop=True)
    data_sorted['Rank'] = range(1, len(data_sorted) + 1)

    # Format scores for display
    data_sorted['FormattedScore'] = data_sorted['ScaledOverallScore'].round(2)

    return data_sorted

# Main Streamlit app
def main():
    st.title("Best-Performing Student Recognition System")

    # Upload CSV
    uploaded_file = st.file_uploader("Upload student dataset (CSV file)", type="csv")

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        if data is not None:
            st.write("Dataset Preview:")
            st.write(data.head(10))

            # Preprocess data
            data_preprocessed = preprocess_data(data)
            data_ranked = rank_students(data_preprocessed)

            # Display top 3 students
            st.subheader("Top 3 Students:")
            st.table(data_ranked[['Rank', 'StudentID', 'Name', 'FormattedScore']].head(3))

            # Query Student Details with Button
            st.subheader("Query a Student's Details:")
            query_id = st.text_input("Enter Student ID:")
            submit_button = st.button("Check Student Details")

            if submit_button:
                if query_id:
                    student = data_ranked[data_ranked['StudentID'].astype(str) == query_id]
                    if not student.empty:
                        st.subheader(f"Details for Student ID {query_id}:")
                        student_details = student.iloc[0]
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

if __name__ == "__main__":
    main()