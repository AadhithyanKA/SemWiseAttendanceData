# How to Build Windows .exe (Without a Windows Machine)

Since you do not have a Windows machine, the easiest way to build the executable is to use **GitHub Actions**.

I have already configured a workflow for you.

## Instructions

1.  **Push your code to GitHub**:
    Simply push your changes to your GitHub repository:
    ```bash
    git add .
    git commit -m "Add Windows build workflow"
    git push origin main
    ```

2.  **Wait for the Build**:
    - Go to your repository on GitHub.
    - Click on the **Actions** tab.
    - You should see a workflow named "Build Windows Executable" running.

3.  **Download the App**:
    - Once the workflow finishes (green checkmark), click on it.
    - Scroll down to the **Artifacts** section.
    - Click on `AttendanceApp-Windows` to download a zip file containing your Windows application.

## Running the App on Windows
1.  Unzip the downloaded file on a Windows computer.
2.  Open the folder.
3.  Double-click `AttendanceApp.exe` (it might be inside a `AttendanceApp` folder).
4.  The application will launch in a terminal window and open your default web browser.

Note: Since the app is not signed with a digital certificate, Windows Defender might warn you. You can click "More info" -> "Run anyway".
