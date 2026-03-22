import os
import sys
import subprocess


def _suprimir_janela_subprocess() -> None:
    """
    Em apps PyInstaller sem console (console=False), cada subprocess filho
    (ex: FFmpeg chamado pelo Whisper) abre e fecha um terminal rapidamente.
    Esse patch garante CREATE_NO_WINDOW em todos os subprocess no Windows.
    """
    if sys.platform != "win32":
        return
    _orig = subprocess.Popen.__init__

    def _patched(self, args, **kwargs):
        kwargs.setdefault("creationflags", 0)
        kwargs["creationflags"] |= subprocess.CREATE_NO_WINDOW
        _orig(self, args, **kwargs)

    subprocess.Popen.__init__ = _patched


# Aplica imediatamente ao ser importado (antes de qualquer outro import)
_suprimir_janela_subprocess()


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
