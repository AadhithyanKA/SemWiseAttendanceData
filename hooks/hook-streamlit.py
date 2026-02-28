# PyInstaller hook for Streamlit
from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('streamlit')
