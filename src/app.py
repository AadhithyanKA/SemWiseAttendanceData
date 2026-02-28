import streamlit as st
import pandas as pd
import io
from generate_reports import load_data, generate_student_report, generate_summary_report

st.set_page_config(page_title="Attendance Report Generator", layout="wide")

st.title("Attendance Report Generator")
st.write("Upload your attendance data (CSV or Excel) to generate the Student-wise and Summary reports.")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load data
        with st.spinner("Loading data..."):
            df = load_data(uploaded_file)
        
        st.success("Data loaded successfully!")
        
        # Show raw data preview
        with st.expander("Preview Raw Data"):
            st.dataframe(df.head())
        
        # Generate reports
        with st.spinner("Generating reports..."):
            student_report = generate_student_report(df)
            summary_report = generate_summary_report(df)
            
        # Dashboard Overview
        st.header("Dashboard Overview")
        
        # Calculate overall metrics from student report
        total_students = len(student_report)
        avg_attendance = student_report['Overall %'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Students", total_students)
        col2.metric("Average Attendance", f"{avg_attendance:.1f}%")
        
        # Visualizations for Summary Report
        if not summary_report.empty:
            # Filter out "Total" row for plotting
            plot_df = summary_report[summary_report['Department'] != 'Total:'].copy()
            
            # Clean percentage columns for plotting
            def clean_pct(val):
                if isinstance(val, str) and '%' in val:
                    return float(val.replace('%', ''))
                return val

            # Check if columns exist
            if 'Above 75%' in plot_df.columns:
                 plot_df['Above 75%'] = plot_df['Above 75%'].apply(clean_pct)
            if 'Below 75%' in plot_df.columns:
                 plot_df['Below 75%'] = plot_df['Below 75%'].apply(clean_pct)
            
            st.subheader("Attendance Distribution by Department/Semester")
            
            # Create a chart if columns exist
            if 'Above 75%' in plot_df.columns and 'Below 75%' in plot_df.columns:
                # Need to convert back to float in case they were strings
                chart_data = plot_df[['Department', 'Semester', 'Above 75%', 'Below 75%']].copy()
                chart_data['Group'] = chart_data['Department'] + " - " + chart_data['Semester']
                chart_data = chart_data.set_index('Group')[['Above 75%', 'Below 75%']]
                st.bar_chart(chart_data)

        st.header("Detailed Reports")
        
        tab1, tab2 = st.tabs(["Student Wise Report", "Summary Report"])
        
        with tab1:
            st.dataframe(student_report)
            
        with tab2:
            st.dataframe(summary_report)
            
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            student_report.to_excel(writer, sheet_name='Student Wise', index=False)
            summary_report.to_excel(writer, sheet_name='Summary', index=False)
        
        output.seek(0)
        
        st.download_button(
            label="Download Excel Report",
            data=output,
            file_name="attendance_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.markdown("### Instructions")
st.markdown("""
1. Upload a CSV or Excel file containing the attendance data.
2. The file must contain the following columns:
   - Roll No.
   - Student Name
   - Department
   - Semester
   - Course Code
   - Hours Conducted
   - Hours Attended
   - Physical Attendance %
3. Click 'Download Excel Report' to save the generated reports.
""")
