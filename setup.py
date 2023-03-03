import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {
#     "excludes": ["tkinter", "unittest"],
#     "zip_include_packages": ["encodings", "PySide6"],
# }

# base="Win32GUI" should be used only for Windows GUI app
base = None

if sys.platform == "win32":
    base = "Win32GUI"

# print(sys.platform)

# base = sys.platform = "Win32GUI"

setup(
    name="TachTachLogoInsertion",
    version="0.1",
    description="Add Tach Tach and FPT logo to images",
    # options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)
