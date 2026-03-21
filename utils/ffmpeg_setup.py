import os
import sys


def configurar_ffmpeg() -> None:
    """
    Garante que o ffmpeg está no PATH antes de qualquer import do whisper.
    Busca em ordem:
      1. sys._MEIPASS/ffmpeg/bin/  (PyInstaller bundle)
      2. ./ffmpeg/bin/             (ffmpeg embutido no projeto)
      3. C:\\ffmpeg\\bin\\
      4. C:\\ffmpeg\\
      5. C:\\Program Files\\ffmpeg\\bin\\
    """
    candidatos = []

    # 1. PyInstaller bundle
    if hasattr(sys, "_MEIPASS"):
        candidatos.append(os.path.join(sys._MEIPASS, "ffmpeg", "bin"))

    # 2. Pasta local ao script/exe
    base = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    candidatos.append(os.path.join(base, "..", "ffmpeg", "bin"))

    # 3-5. Caminhos padrão do sistema
    candidatos += [
        r"C:\ffmpeg\bin",
        r"C:\ffmpeg",
        r"C:\Program Files\ffmpeg\bin",
    ]

    for caminho in candidatos:
        caminho = os.path.normpath(caminho)
        if os.path.exists(os.path.join(caminho, "ffmpeg.exe")):
            # Coloca na frente do PATH para ter precedência
            os.environ["PATH"] = caminho + os.pathsep + os.environ.get("PATH", "")
            return


def get_ffmpeg_path() -> str | None:
    """Retorna o caminho do ffmpeg.exe encontrado ou None."""
    for p in os.environ.get("PATH", "").split(os.pathsep):
        exe = os.path.join(p, "ffmpeg.exe")
        if os.path.exists(exe):
            return exe
    return None
