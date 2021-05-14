import sys
from cx_Freeze import setup, Executable

# criar a build do programa -> python setup.py build

build_exe_options = {"include_files": ['./shortcuts/', 'sabi.ico'], "include_msvcr": True}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="atualizador do Sabi",
    version="0.1",
    description="Atualizador do Sabi!",
    options={"build_exe": build_exe_options},
    executables=[Executable("Atualizador.py", base=base, icon='sabi.ico')]
)
