# Configurar ffmpeg no PATH ANTES de qualquer import do whisper
from utils.ffmpeg_setup import configurar_ffmpeg
configurar_ffmpeg()

import customtkinter as ctk
from ui.app import AptApp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    AptApp().mainloop()
