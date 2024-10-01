import tkinter as tk
from tkinter import filedialog
import whisper
import os
import platform
from tqdm import tqdm

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder.set(folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder.set(folder_selected)

def start_transcription():
    model_choice = model_var.get()
    model = whisper.load_model(model_choice)

    input_path = input_folder.get()
    output_path = output_folder.get()

    # Cria um arquivo de saída único
    output_file = os.path.join(output_path, "transcricoes.txt")
    with open(output_file, "w") as f:
        f.write("")

    total_files = len([f for f in os.listdir(input_path) if f.endswith((".m4a", ".ogg", ".wav", ".mp3"))])
    with tqdm(total=total_files, desc="Transcrevendo áudios") as pbar:
        for filename in os.listdir(input_path):
            if filename.endswith((".m4a", ".ogg", ".wav", ".mp3")):
                audio_path = os.path.join(input_path, filename)
                print(f"Iniciando transcrição de {filename}")
                try:
                    transcription = model.transcribe(audio_path)
                    with open(output_file, "a") as f:
                        f.write(f"\n{filename}:\n{transcription['text']}\n")
                    pbar.update(1)

                    # Atualiza o rótulo de progresso na interface gráfica
                    progress_percentage = int((pbar.n / total_files) * 100)
                    progress_label.config(text=f"Progresso: {progress_percentage}%")
                    if progress_percentage == 100:
                        progress_label.config(fg="purple") # Muda a cor do texto para roxo
                    root.update_idletasks()  # Atualiza a interface imediatamente

                except Exception as e:
                    print(f"Erro ao processar {filename}: {str(e)}")
                    pbar.update(1)

    tk.messagebox.showinfo("Concluído!", "Transcrição finalizada com sucesso!")

# Interface gráfica
root = tk.Tk()
root.title("ApT - Áudio para Texto")

# Detecta o sistema operacional e define o ícone
os_type = platform.system()
icon_path = os.path.join("images", f"app_icon.{'ico' if os_type == 'Windows' else 'png'}")
if os.path.exists(icon_path):
    try:
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(False, icon_image)
    except tk.TclError as e:
        print(f"Erro ao carregar o ícone: {e}")

# Variáveis para pastas e modelo
input_folder = tk.StringVar()
output_folder = tk.StringVar()
model_var = tk.StringVar(value="base")

# Label para a barra de progresso
progress_label = tk.Label(root, text="Progresso: 0%")
progress_label.pack()

# Labels e entradas de pastas
tk.Label(root, text="Pasta de entrada:").pack()
tk.Entry(root, textvariable=input_folder, width=50).pack()
tk.Button(root, text="Selecionar pasta", command=select_input_folder).pack()

tk.Label(root, text="Pasta de saída:").pack()
tk.Entry(root, textvariable=output_folder, width=50).pack()
tk.Button(root, text="Selecionar pasta", command=select_output_folder).pack()

# Radiobuttons para escolha do modelo
tk.Label(root, text="Escolha o modelo Whisper:").pack()
tk.Radiobutton(root, text="base", variable=model_var, value="base").pack()
tk.Radiobutton(root, text="medium",variable=model_var, value="medium").pack()
tk.Radiobutton(root, text="large",variable=model_var, value="large").pack()

# Botão para iniciar a transcrição
tk.Button(root, text="Iniciar Transcrição", bg="purple", fg="white", command=start_transcription).pack()

root.mainloop()
