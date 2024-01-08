import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["arayuz", "fonksiyonlar", "vt", "tkcalendar", "mysql.connector", "TKinterModernThemes", "numpy", "matplotlib"],
    "include_files": ["icon.ico"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(
    script="main.py",
    base=base,
    icon="icon.ico"
)

setup(
    name="Personel Takip Sistemi",
    version="1.0",
    description="",
    options={"build_exe": build_exe_options},
    executables=[exe]
)