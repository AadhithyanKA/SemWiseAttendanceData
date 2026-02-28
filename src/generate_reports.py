import pandas as pd
import os
import argparse

REQUIRED_COLUMNS = [
    "S No.", "Roll No.", "Student Name", "School", "Department", "Program",
    "Semester", "Batch", "Course Code", "Course Name", "Hours Conducted",
    "Hours Attended", "Physical Attendance %", "Approved Leave Hours",
    "Approved Leave %", "Attended Hours with Approved Leave",
    "Attended Hours with Approved Leave Percentage", "Staff Name"
]

def load_data(file_input):
    """
    Load attendance data from a CSV or Excel file (path or buffer).
    """
    # Check if input is a string (path) or a buffer
    is_path = isinstance(file_input, str)
    
    if is_path and not os.path.exists(file_input):
        raise FileNotFoundError(f"File not found: {file_input}")

    try:
        if is_path:
            if file_input.endswith('.csv'):
                df = pd.read_csv(file_input)
            elif file_input.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_input)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        else:
            # Assume buffer, try to determine type from name attribute if available, else try both
            if hasattr(file_input, 'name'):
                if file_input.name.endswith('.csv'):
                    df = pd.read_csv(file_input)
                else:
                    df = pd.read_excel(file_input)
            else:
                 # Fallback: try excel then csv
                 try:
                     df = pd.read_excel(file_input)
                 except:
                     file_input.seek(0)
                     df = pd.read_csv(file_input)
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    if is_path:
        # For buffers, we can't easily check 'endswith' without 'name', handled above
        pass

    # Validate columns (check for subset or key columns)
    # Note: We are flexible if some non-critical columns are missing, but need the keys.
    critical_columns = ["Roll No.", "Student Name", "Department", "Semester", "Course Code", "Hours Conducted", "Hours Attended", "Physical Attendance %"]
    missing_columns = [col for col in critical_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing critical columns: {missing_columns}")
    
    return df

def generate_student_report(df):
    """
    Generate Report 1: Student-wise Course Attendance Summary
    """
    # Define grouping columns (Student Identifiers)
    # We include School, Department, Program, Semester, Batch to keep them in the report
    # assuming they are constant for a student.
    group_cols = ["Roll No.", "Student Name", "School", "Department", "Program", "Semester", "Batch"]
    
    # Check which of these actually exist in df to be safe
    existing_group_cols = [col for col in group_cols if col in df.columns]
    
    # Group by student
    grouped = df.groupby(existing_group_cols)
    
    report_data = []
    
    for name, group in grouped:
        # name is a tuple of the grouping values
        student_info = dict(zip(existing_group_cols, name))
        
        total_courses = len(group)
        # Assuming 'Physical Attendance %' is numeric. If not, we might need to clean it.
        # Clean % column if necessary (remove % sign)
        if group['Physical Attendance %'].dtype == 'O':
             group['Physical Attendance %'] = group['Physical Attendance %'].astype(str).str.replace('%', '').astype(float)
        
        less_than_75 = (group['Physical Attendance %'] < 75).sum()
        between_75_100 = (group['Physical Attendance %'] >= 75).sum()
        
        tcc = group['Hours Conducted'].sum()
        tca = group['Hours Attended'].sum()
        
        overall_percentage = (tca / tcc * 100) if tcc > 0 else 0
        
        row = {
            # "Sl.No": 0, # Will be added later
            "School": student_info.get("School", ""),
            "Department": student_info.get("Department", ""),
            "Program": student_info.get("Program", ""),
            "Semester": student_info.get("Semester", ""),
            "Batch": student_info.get("Batch", ""),
            "Roll No.": student_info.get("Roll No.", ""),
            "Student Name": student_info.get("Student Name", ""),
            "Total Courses": total_courses,
            "<75": less_than_75,
            "75-100": between_75_100,
            "TCC": tcc,
            "TCA": tca,
            "Overall %": round(overall_percentage, 2),
            "Remarks": "" # Placeholder
        }
        report_data.append(row)
        
    report_df = pd.DataFrame(report_data)
    # Add Sl.No
    report_df.insert(0, 'Sl.No', range(1, 1 + len(report_df)))
    
    return report_df

def generate_summary_report(df):
    """
    Generate Report 2: Department/Semester-wise Summary
    """
    # First, we need student-level aggregation to classify each student
    # Group by Department, Semester, and Student (Roll No)
    student_group_cols = ["Department", "Semester", "Roll No."]
    existing_cols = [col for col in student_group_cols if col in df.columns]
    
    # Pre-process percentages
    if df['Physical Attendance %'].dtype == 'O':
         df['Physical Attendance %'] = df['Physical Attendance %'].astype(str).str.replace('%', '').astype(float)

    # We need to know for each student:
    # 1. Are all their courses >= 75%?
    # 2. Are all their courses < 75%?
    # 3. Do they have >= 1 course < 75%?
    
    # Helper to aggregate at student level
    def analyze_student(x):
        all_above_75 = (x['Physical Attendance %'] >= 75).all()
        all_below_75 = (x['Physical Attendance %'] < 75).all()
        any_below_75 = (x['Physical Attendance %'] < 75).any()
        return pd.Series({
            'all_above_75': all_above_75,
            'all_below_75': all_below_75,
            'any_below_75': any_below_75
        })

    student_stats = df.groupby(existing_cols).apply(analyze_student).reset_index()
    
    # Now group by Department and Semester to count these students
    dept_sem_grouped = student_stats.groupby(["Department", "Semester"])
    
    summary_data = []
    
    for (dept, sem), group in dept_sem_grouped:
        student_strength = len(group)
        
        above_75_all_count = group['all_above_75'].sum()
        above_75_pct = (above_75_all_count / student_strength * 100) if student_strength > 0 else 0
        
        # Below 75% is the complement of Above 75% (i.e., students who have at least one course < 75%)
        # Alternatively, it is group['any_below_75'].sum()
        # Let's verify: all_above_75 is True only if NO course is < 75. 
        # So any_below_75 should be the exact inverse.
        below_75_pct = 100 - above_75_pct
        
        less_than_75_one_plus_count = group['any_below_75'].sum()
        less_than_75_one_plus_pct = (less_than_75_one_plus_count / student_strength * 100) if student_strength > 0 else 0
        
        less_than_75_all_count = group['all_below_75'].sum()
        less_than_75_all_pct = (less_than_75_all_count / student_strength * 100) if student_strength > 0 else 0
        
        row = {
            "Department": dept,
            "Semester": sem,
            "Student Strength": student_strength,
            "Above 75% in All Courses": above_75_all_count,
            "Above 75%": f"{round(above_75_pct, 0)}%", # Formatting as string with % as per example
            "Below 75%": f"{round(below_75_pct, 0)}%",
            "Less than 75% (1+ Courses)": less_than_75_one_plus_count,
            "Less than 75% 1+ Courses (%)": f"{round(less_than_75_one_plus_pct, 0)}%",
            "Less than 75% (All Courses)": less_than_75_all_count,
            "% of <75% (All Courses)": f"{round(less_than_75_all_pct, 0)}%"
        }
        summary_data.append(row)
        
    summary_df = pd.DataFrame(summary_data)
    
    # Add Total Row
    if not summary_df.empty:
        total_strength = summary_df["Student Strength"].sum()
        total_above_75_all = summary_df["Above 75% in All Courses"].sum()
        total_less_one_plus = summary_df["Less than 75% (1+ Courses)"].sum()
        total_less_all = summary_df["Less than 75% (All Courses)"].sum()
        
        total_above_pct = (total_above_75_all / total_strength * 100) if total_strength > 0 else 0
        total_below_pct = 100 - total_above_pct
        total_less_one_plus_pct = (total_less_one_plus / total_strength * 100) if total_strength > 0 else 0
        total_less_all_pct = (total_less_all / total_strength * 100) if total_strength > 0 else 0
        
        total_row = {
            "Department": "Total:",
            "Semester": "",
            "Student Strength": total_strength,
            "Above 75% in All Courses": total_above_75_all,
            "Above 75%": f"{round(total_above_pct, 0)}%",
            "Below 75%": f"{round(total_below_pct, 0)}%",
            "Less than 75% (1+ Courses)": total_less_one_plus,
            "Less than 75% 1+ Courses (%)": f"{round(total_less_one_plus_pct, 0)}%",
            "Less than 75% (All Courses)": total_less_all,
            "% of <75% (All Courses)": f"{round(total_less_all_pct, 0)}%"
        }
        
        summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)

    return summary_df

def main():
    parser = argparse.ArgumentParser(description="Generate Attendance Reports")
    parser.add_argument("--input", default="data/sample_attendance.csv", help="Input CSV/Excel file path")
    parser.add_argument("--output", default="output/attendance_report.xlsx", help="Output Excel file path")
    args = parser.parse_args()
    
    try:
        print(f"Loading data from {args.input}...")
        df = load_data(args.input)
        
        print("Generating Student Report...")
        student_report = generate_student_report(df)
        
        print("Generating Summary Report...")
        summary_report = generate_summary_report(df)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        
        print(f"Saving reports to {args.output}...")
        with pd.ExcelWriter(args.output, engine='openpyxl') as writer:
            student_report.to_excel(writer, sheet_name='Student Wise', index=False)
            summary_report.to_excel(writer, sheet_name='Summary', index=False)
            
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
