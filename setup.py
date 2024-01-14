import sys
from cx_Freeze import setup, Executable

# cx_Freeze için yapılandırma seçenekleri
build_exe_options = {
    "packages": ["arayuz", "fonksiyonlar", "vt", "tkcalendar", "mysql.connector", "TKinterModernThemes", "numpy", "matplotlib"],
    "include_files": ["icon.ico"]
}

# Uygulama penceresi tipini belirleme
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executable nesnesini oluşturma
exe = Executable(
    script="main.py",
    base=base,
    icon="icon.ico"
)

# cx_Freeze setup fonksiyonu çağrısı
setup(
    name="Personel Takip Sistemi",
    version="1.0",
    description="",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
