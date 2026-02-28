# SemWiseAttendanceData

This project processes student attendance data to generate detailed reports.

## Features

- **Student-wise Report**: Detailed attendance statistics for each student across all enrolled courses.
- **Summary Report**: Department and Semester-wise aggregation of attendance performance.

## Setup

1. **Install Dependencies**:
   Ensure you have Python installed.
   ```bash
   pip install -r requirements.txt
   ```
   Or use the provided `run.sh` script which handles virtual environment creation.

2. **Prepare Data**:
   Place your attendance data (CSV or Excel) in the `data/` directory.
   The input file must have columns like:
   - Roll No.
   - Student Name
   - Department
   - Semester
   - Course Code
   - Hours Conducted
   - Hours Attended
   - Physical Attendance %

   See `data/sample_attendance.csv` for an example format.

## Usage

### Option 1: Web App (Recommended)
Launch the interactive web interface to upload files and download reports.

```bash
./run.sh app
```
Or manually:
```bash
streamlit run src/app.py
```

### Option 2: Command Line Interface (CLI)
Generate reports directly from the terminal.

```bash
./run.sh
```
This will process `data/sample_attendance.csv` and save the report to `output/attendance_report.xlsx`.

To specify custom input/output files:
```bash
python src/generate_reports.py --input path/to/data.csv --output path/to/report.xlsx
```

## Reports Generated

The output Excel file contains two sheets:
1. **Student Wise**: Individual student performance metrics.
2. **Summary**: Aggregate metrics grouped by Department and Semester.
