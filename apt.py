import tkinter as tk
from tkinter import filedialog
import whisper
import os
import platform  # Importa a biblioteca para detectar o sistema operacional


# Função para escolher pasta de entrada
def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder.set(folder_selected)

# Função para escolher pasta de saída
def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder.set(folder_selected)

# Função para iniciar a transcrição
def start_transcription():
    model_choice = model_var.get()  # Pega a escolha do modelo
    model = whisper.load_model(model_choice)
    
    input_path = input_folder.get()
    output_path = output_folder.get()

    for filename in os.listdir(input_path):
        if filename.endswith((".m4a", ".ogg", ".wav", ".mp3")):
            audio_path = os.path.join(input_path, filename)
            transcription = model.transcribe(audio_path)
            
            output_file = os.path.join(output_path, f"{filename}.txt")
            with open(output_file, "w") as f:
                f.write(transcription['text'])

# Interface gráfica
root = tk.Tk()
root.title("ApT - Áudio para Texto")

# Detecta o sistema operacional
os_type = platform.system()

# Define o ícone baseado no sistema operacional e na pasta 'images'
if os_type == "Windows":
    icon_path = os.path.join("images", "app_icon.ico")  # Ícone no formato .ico para Windows
elif os_type == "Darwin":  # macOS
    icon_path = os.path.join("images", "app_icon.png")  # Ícone no formato .png para macOS
else:
    icon_path = os.path.join("images", "app_icon.png")  # Ícone genérico para Linux (geralmente .png)

# Adicionar ícone à janela (somente se o arquivo de ícone existir)
if os.path.exists(icon_path):
    icon_image = tk.PhotoImage(file=icon_path)
    root.iconphoto(False, icon_image)

input_folder = tk.StringVar()
output_folder = tk.StringVar()

tk.Label(root, text="Pasta de entrada:").pack()
tk.Entry(root, textvariable=input_folder, width=50).pack()
tk.Button(root, text="Selecionar pasta", command=select_input_folder).pack()

tk.Label(root, text="Pasta de saída:").pack()
tk.Entry(root, textvariable=output_folder, width=50).pack()
tk.Button(root, text="Selecionar pasta", command=select_output_folder).pack()

tk.Label(root, text="Escolha o modelo Whisper:").pack()
model_var = tk.StringVar(value="base")
tk.Radiobutton(root, text="base", variable=model_var, value="base").pack()
tk.Radiobutton(root, text="medium", variable=model_var, value="medium").pack()
tk.Radiobutton(root, text="large", variable=model_var, value="large").pack()

tk.Button(root, text="Iniciar Transcrição", command=start_transcription).pack()

root.mainloop()
