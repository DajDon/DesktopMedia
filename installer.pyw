import customtkinter as ctk
import os
import requests
from pathlib import Path
import subprocess
import sys

root = ctk.CTk()
root.title("DesktopMedia - Installer")
root.geometry("450x200")
root.config(background="#16191d")
root.resizable(False, False)


def resource_path(path):
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / path
    return Path(__file__).parent / path
root.iconbitmap(str(resource_path("assets/logo.ico")))

def download():
    try:
        status.configure(text="Downloading...")
        root.update_idletasks()
        app = Path(os.getenv("LOCALAPPDATA")) / "DesktopMedia"
        app.mkdir(parents=True, exist_ok=True)
        url = "https://github.com/DajDon/DesktopMedia/releases/latest/download/DesktopMedia.v1.1.exe"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        file_path = app / "DesktopMedia.v1.1.exe"
        file_path.write_bytes(r.content)
        shortcut = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/DesktopMedia.lnk"
        subprocess.run([
            "powershell", "-Command",
            f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut}');$s.TargetPath='{file_path}';$s.IconLocation='{file_path},0';$s.Save()"
        ])
        status.configure(text="Success!")
    except Exception as e:
        status.configure(text="Error!")
        print(e)
        
installer_title = ctk.CTkLabel(
    root,
    text="Installer",
    font=("Arial", 40, "bold"),
    text_color="white",
    fg_color="#16191d"
)
installer_title.place(relx=0.5, rely=0.2, anchor="center")

installer_btn = ctk.CTkButton(
    root,
    text="Install",
    width=200,
    height=50,
    command=download,
    fg_color="#029cff",
    hover_color="#0293ec",
    font=("Arial", 25)
)
installer_btn.place(relx=0.5, rely=0.7, anchor="center")

status = ctk.CTkLabel(
    root,
    text="",
    fg_color="#16191d"
)
status.place(relx=0.5, rely=0.5, anchor="center")

root.mainloop()