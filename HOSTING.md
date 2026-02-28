# Hosting the App on Local Network

To access the app via `psod.local.app/attendance` from other computers on your network, follow these steps.

## 1. Run the App as Server
You need to run the application with specific settings to make it accessible to other devices.

1.  Locate `run_host.bat` in the `dist/AttendanceApp` folder (it is included in the build).
2.  **Right-click** on `run_host.bat` and select **Run as Administrator**.
    -   *Why Administrator?* Because accessing port 80 (standard HTTP port) requires admin privileges on Windows.
    -   If you don't run as admin, it might fail to start. In that case, edit the bat file to use a different port (e.g., 8501).

## 2. Configure DNS (Crucial Step)
For other computers to recognize the name `psod.local.app`, they need to know which IP address it belongs to.

### Option A: Router DNS (Best for "Everyone")
If you have access to your Router's configuration:
1.  Find the "DNS", "Local DNS", or "Static Leases" section.
2.  Add a record:
    -   **Hostname**: `psod.local.app`
    -   **IP Address**: The IP address of the computer running the app (e.g., `192.168.1.50`).

### Option B: Hosts File (Per Computer)
If you cannot configure the router, you must edit the `hosts` file on **each computer** that wants to access the app.

**On Windows Clients:**
1.  Open Notepad as Administrator.
2.  Open `C:\Windows\System32\drivers\etc\hosts`.
3.  Add this line at the bottom:
    ```
    192.168.1.XX  psod.local.app
    ```
    (Replace `192.168.1.XX` with the Server's IP address).

## 3. Access the App
Once running and DNS is configured:
-   Open browser and go to: `http://psod.local.app/attendance`

### Troubleshooting
-   **Firewall**: Ensure Windows Firewall allows incoming connections on Port 80 (or the port you used).
-   **IP Address Changes**: If your server's IP changes (DHCP), the DNS mapping will break. Set a Static IP for the server if possible.
