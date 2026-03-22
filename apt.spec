# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para o ApT — Áudio para Texto
Gera: dist/ApT/ApT.exe  (modo onedir — FFmpeg incluído)

Como usar:
    1. Certifique-se de ter o ffmpeg.exe, ffprobe.exe e ffplay.exe dentro de
       uma subpasta  apt/ffmpeg/bin/  (copie de https://www.gyan.dev/ffmpeg/builds/)
    2. Ative o .venv:  .venv\\Scripts\\activate
    3. Instale o PyInstaller:  pip install pyinstaller
    4. Gere o executável:  pyinstaller apt.spec
    5. O resultado estará em  dist/ApT/ApT.exe

Notas:
    - Os modelos Whisper são baixados na primeira execução e ficam em cache
      em %USERPROFILE%\\.cache\\whisper  (não são empacotados — são grandes demais)
    - O arquivo .apt_license (estado gratuito) fica junto ao ApT.exe em dist/ApT/
    - O arquivo .apt_lic (licença premium) é carregado pelo usuário via interface
"""

import sys
from pathlib import Path

block_cipher = None

# Caminho raiz do projeto
ROOT = Path(SPECPATH)

# Verifica se o FFmpeg local existe
FFMPEG_BIN = ROOT / "ffmpeg" / "bin"
has_ffmpeg = FFMPEG_BIN.exists()
if not has_ffmpeg:
    print(
        "\n⚠️  AVISO: pasta ffmpeg/bin/ não encontrada.\n"
        "   Baixe o FFmpeg em https://www.gyan.dev/ffmpeg/builds/\n"
        "   e coloque ffmpeg.exe, ffprobe.exe e ffplay.exe em apt/ffmpeg/bin/\n"
    )

a = Analysis(
    ["main.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Ícones e imagens
        (str(ROOT / "images"), "images"),
        # FFmpeg embutido (se existir)
        *([(str(FFMPEG_BIN / "ffmpeg.exe"), "ffmpeg/bin"),
           (str(FFMPEG_BIN / "ffprobe.exe"), "ffmpeg/bin"),
           (str(FFMPEG_BIN / "ffplay.exe"), "ffmpeg/bin")] if has_ffmpeg else []),
        # Assets do CustomTkinter (temas e fontes)
        ("customtkinter", "customtkinter"),
    ],
    hiddenimports=[
        # Whisper
        "whisper",
        "whisper.audio",
        "whisper.model",
        "whisper.tokenizer",
        "whisper.utils",
        "whisper.decoding",
        "whisper.transcribe",
        # Torch
        "torch",
        "torch.nn",
        "tqdm",
        "tiktoken",
        "tiktoken_ext",
        "tiktoken_ext.openai_public",
        # Crypto
        "cryptography",
        "cryptography.hazmat.primitives.asymmetric.ed25519",
        "cryptography.hazmat.primitives.serialization",
        "cryptography.exceptions",
        # Audio/PDF
        "mutagen",
        "reportlab",
        "reportlab.pdfgen",
        "reportlab.lib",
        # UI
        "customtkinter",
        "tkinter",
        "tkinter.filedialog",
        "tkinter.messagebox",
        # Outros
        "PIL",
        "packaging",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "scipy",
        "pandas",
        "IPython",
        "jupyter",
        "notebook",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ApT",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,           # sem janela de terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ROOT / "images" / "apt_text.ico"),
    version_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ApT",
)
