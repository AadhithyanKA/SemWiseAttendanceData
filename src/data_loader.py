import pandas as pd
import os

REQUIRED_COLUMNS = [
    "S No.", "Roll No.", "Student Name", "School", "Department", "Program",
    "Semester", "Batch", "Course Code", "Course Name", "Hours Conducted",
    "Hours Attended", "Physical Attendance %", "Approved Leave Hours",
    "Approved Leave %", "Attended Hours with Approved Leave",
    "Attended Hours with Approved Leave Percentage", "Staff Name"
]

def load_data(file_path):
    """
    Load attendance data from a CSV or Excel file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    # Validate columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following columns are missing from the data: {missing_columns}")
    
    return df

def main():
    # Example usage
    sample_file = "../data/sample_attendance.csv"
    try:
        df = load_data(sample_file)
        print("Data loaded successfully:")
        print(df.head())
        print("\nColumn types:")
        print(df.dtypes)
    except Exception as e:
        print(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
