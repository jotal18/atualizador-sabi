import sys
from cx_Freeze import setup, Executable

# criar a build do programa -> python setup.py build

build_exe_options = {"include_files": ['./shortcuts/']}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="guifoo",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
