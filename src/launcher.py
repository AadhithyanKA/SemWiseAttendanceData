import sys
import os
import streamlit.web.cli as stcli

def resolve_path(path):
    if getattr(sys, "frozen", False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

if __name__ == "__main__":
    # In frozen app, app.py is at root of _MEIPASS
    if getattr(sys, "frozen", False):
        app_path = resolve_path("app.py")
    else:
        app_path = resolve_path("app.py")

    # Configure streamlit args
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
    ]
    
    sys.exit(stcli.main())
