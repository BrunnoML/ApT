import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os
import shutil

# Garante que o ffmpeg está no PATH independente do terminal usado
_FFMPEG_PATHS = [r"C:\ffmpeg\bin", r"C:\ffmpeg", r"C:\Program Files\ffmpeg\bin"]
for _p in _FFMPEG_PATHS:
    if os.path.exists(os.path.join(_p, "ffmpeg.exe")):
        os.environ["PATH"] = _p + os.pathsep + os.environ.get("PATH", "")
        break
import platform
import hashlib
import socket
import json
from datetime import datetime
from tqdm import tqdm
from mutagen import File as MutagenFile
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ─────────────────────────────────────────────
# Arquivo de controle de licença (local)
# ─────────────────────────────────────────────
LICENSE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".apt_license")
MAX_FREE_LAUDOS = 1


def laudos_gerados():
    """Retorna o número de laudos já gerados na versão gratuita."""
    if not os.path.exists(LICENSE_FILE):
        return 0
    try:
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
            return data.get("laudos", 0)
    except Exception:
        return 0


def registrar_laudo():
    """Incrementa o contador de laudos gerados."""
    count = laudos_gerados() + 1
    with open(LICENSE_FILE, "w") as f:
        json.dump({"laudos": count}, f)


def tem_licenca():
    """Verifica se existe licença ativa (versão futura)."""
    if not os.path.exists(LICENSE_FILE):
        return False
    try:
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
            return data.get("licenca_ativa", False)
    except Exception:
        return False


def pode_gerar_laudo():
    """Retorna True se o usuário pode gerar um novo laudo."""
    return tem_licenca() or laudos_gerados() < MAX_FREE_LAUDOS


# ─────────────────────────────────────────────
# Utilitários
# ─────────────────────────────────────────────
def calcular_hash(filepath):
    """Calcula o hash SHA-256 do arquivo antes de qualquer processamento."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def obter_duracao(filepath):
    """Retorna a duração do áudio em segundos usando mutagen."""
    try:
        audio = MutagenFile(filepath)
        if audio is not None and hasattr(audio.info, "length"):
            segundos = int(audio.info.length)
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            segs = segundos % 60
            if horas > 0:
                return f"{horas:02d}:{minutos:02d}:{segs:02d}"
            return f"{minutos:02d}:{segs:02d}"
    except Exception:
        pass
    return "Indisponível"


def segundos_totais(filepath):
    """Retorna duração em segundos para somar no relatório."""
    try:
        audio = MutagenFile(filepath)
        if audio is not None and hasattr(audio.info, "length"):
            return int(audio.info.length)
    except Exception:
        pass
    return 0


def formatar_duracao_total(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"
    return f"{minutos:02d}:{segs:02d}"


# ─────────────────────────────────────────────
# Geração do laudo PDF
# ─────────────────────────────────────────────
def gerar_laudo_pdf(output_path, unidade, responsavel, modelo, arquivos_dados, hash_txt=None):
    """
    Gera o laudo forense em PDF.
    arquivos_dados: lista de dicts com nome, hash, duracao, transcricao
    """
    agora = datetime.now()
    nome_arquivo = f"laudo_transcricao_{agora.strftime('%Y%m%d_%H%M%S')}.pdf"
    caminho_pdf = os.path.join(output_path, nome_arquivo)

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        "titulo", parent=estilos["Title"], fontSize=14, spaceAfter=6, alignment=TA_CENTER
    )
    estilo_subtitulo = ParagraphStyle(
        "subtitulo", parent=estilos["Normal"], fontSize=10, spaceAfter=4,
        textColor=colors.HexColor("#444444"), alignment=TA_CENTER
    )
    estilo_secao = ParagraphStyle(
        "secao", parent=estilos["Heading2"], fontSize=11, spaceBefore=12,
        spaceAfter=4, textColor=colors.HexColor("#1a1a2e")
    )
    estilo_label = ParagraphStyle(
        "label", parent=estilos["Normal"], fontSize=9,
        textColor=colors.HexColor("#555555")
    )
    estilo_valor = ParagraphStyle(
        "valor", parent=estilos["Normal"], fontSize=9, fontName="Courier"
    )
    estilo_transcricao = ParagraphStyle(
        "transcricao", parent=estilos["Normal"], fontSize=9,
        leading=14, alignment=TA_JUSTIFY, spaceAfter=6
    )
    estilo_rodape = ParagraphStyle(
        "rodape", parent=estilos["Normal"], fontSize=8,
        textColor=colors.HexColor("#888888"), alignment=TA_CENTER
    )

    conteudo = []

    # ── Cabeçalho ──
    conteudo.append(Paragraph("LAUDO DE TRANSCRIÇÃO DE ÁUDIO", estilo_titulo))
    conteudo.append(Paragraph("Cadeia de Custódia — Lei 13.964/2019 (Pacote Anticrime)", estilo_subtitulo))
    conteudo.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a1a2e")))
    conteudo.append(Spacer(1, 0.4 * cm))

    dados_cabecalho = [
        ["Unidade:", unidade],
        ["Responsável:", responsavel],
        ["Data/Hora do processamento:", agora.strftime("%d/%m/%Y às %H:%M:%S")],
        ["Máquina (hostname):", socket.gethostname()],
        ["Sistema Operacional:", f"{platform.system()} {platform.release()}"],
        ["Ferramenta:", "ApT — Áudio para Texto"],
        ["Modelo Whisper utilizado:", modelo],
        ["Total de arquivos processados:", str(len(arquivos_dados))],
    ]

    # Total de duração somada
    total_seg = sum(a.get("segundos", 0) for a in arquivos_dados)
    dados_cabecalho.append(["Duração total dos áudios:", formatar_duracao_total(total_seg)])

    tabela_cab = Table(dados_cabecalho, colWidths=[6 * cm, 11 * cm])
    tabela_cab.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f5f5f5"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#dddddd")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    conteudo.append(tabela_cab)
    conteudo.append(Spacer(1, 0.5 * cm))

    # ── Por arquivo ──
    for i, arq in enumerate(arquivos_dados, 1):
        conteudo.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
        conteudo.append(Paragraph(f"Arquivo {i} de {len(arquivos_dados)}", estilo_secao))

        dados_arq = [
            ["Nome do arquivo:", arq["nome"]],
            ["Hash SHA-256:", arq["hash"]],
            ["Duração:", arq["duracao"]],
        ]
        tabela_arq = Table(dados_arq, colWidths=[4.5 * cm, 12.5 * cm])
        tabela_arq.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Courier"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f9f9f9"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#dddddd")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        conteudo.append(tabela_arq)
        conteudo.append(Spacer(1, 0.3 * cm))
        conteudo.append(Paragraph("<b>Transcrição:</b>", estilo_label))
        texto = arq["transcricao"].strip().replace("\n", "<br/>")
        conteudo.append(Paragraph(texto if texto else "<i>(sem conteúdo transcrito)</i>", estilo_transcricao))

    conteudo.append(Spacer(1, 0.5 * cm))
    conteudo.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a1a2e")))
    conteudo.append(Spacer(1, 0.3 * cm))

    # ── Declaração de conformidade ──
    conteudo.append(Paragraph(
        "Este laudo foi gerado automaticamente pela ferramenta <b>ApT — Áudio para Texto</b>. "
        "Os hashes SHA-256 foram calculados sobre os arquivos originais antes de qualquer processamento, "
        "preservando a integridade da prova digital conforme exigido pelos arts. 158-A a 158-F do "
        "Código de Processo Penal (Lei 13.964/2019 — Pacote Anticrime).",
        estilo_rodape
    ))

    doc.build(conteudo)

    # ── Hash do próprio PDF gerado ──
    hash_pdf = calcular_hash(caminho_pdf)
    return caminho_pdf, hash_pdf


# ─────────────────────────────────────────────
# Funções da interface
# ─────────────────────────────────────────────
def select_input_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        input_folder.set(os.path.normpath(folder_selected))

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder.set(os.path.normpath(folder_selected))


def start_transcription():
    model_choice = model_var.get()
    input_path = input_folder.get()
    output_path = output_folder.get()
    unidade = unidade_var.get().strip()
    responsavel = responsavel_var.get().strip()
    gerar_pdf = gerar_pdf_var.get()

    if not input_path:
        messagebox.showwarning("Atenção", "Selecione a pasta de entrada.")
        return
    if not output_path:
        messagebox.showwarning("Atenção", "Selecione a pasta de saída.")
        return
    if gerar_pdf and not unidade:
        messagebox.showwarning("Atenção", "Informe a Unidade para gerar o laudo PDF.")
        return
    if gerar_pdf and not responsavel:
        messagebox.showwarning("Atenção", "Informe o Responsável para gerar o laudo PDF.")
        return

    # Verifica limite de laudos gratuitos
    if gerar_pdf and not pode_gerar_laudo():
        messagebox.showinfo(
            "Versão Gratuita",
            f"Você já utilizou o laudo gratuito disponível na versão de teste.\n\n"
            f"Para gerar laudos ilimitados, adquira a licença anual do ApT.\n\n"
            f"Entre em contato para mais informações."
        )
        return

    model = whisper.load_model(model_choice)

    arquivos = [f for f in os.listdir(input_path) if f.endswith((".m4a", ".ogg", ".wav", ".mp3", ".mp4", ".wma"))]
    total_files = len(arquivos)

    if total_files == 0:
        messagebox.showwarning("Atenção", "Nenhum arquivo de áudio encontrado na pasta selecionada.")
        return

    # Arquivo TXT de saída (mantido como hoje)
    output_file = os.path.join(output_path, "transcricoes.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("")

    arquivos_dados = []

    with tqdm(total=total_files, desc="Transcrevendo áudios") as pbar:
        for filename in arquivos:
            audio_path = os.path.normpath(os.path.join(input_path, filename))
            print(f"Iniciando transcrição de {filename}")

            # Hash SHA-256 ANTES do processamento
            hash_arquivo = calcular_hash(audio_path)
            duracao = obter_duracao(audio_path)
            seg = segundos_totais(audio_path)

            try:
                transcription = model.transcribe(audio_path)
                texto = transcription["text"]

                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Arquivo : {filename}\n")
                    f.write(f"Hash    : {hash_arquivo}\n")
                    f.write(f"Duração : {duracao}\n")
                    f.write(f"{'='*60}\n")
                    f.write(f"{texto}\n")

                arquivos_dados.append({
                    "nome": filename,
                    "hash": hash_arquivo,
                    "duracao": duracao,
                    "segundos": seg,
                    "transcricao": texto,
                })

                pbar.update(1)
                progress_percentage = int((pbar.n / total_files) * 100)
                progress_label.config(text=f"Progresso: {progress_percentage}%")
                if progress_percentage == 100:
                    progress_label.config(fg="purple")
                root.update_idletasks()

            except Exception as e:
                print(f"Erro ao processar {filename}: {str(e)}")
                arquivos_dados.append({
                    "nome": filename,
                    "hash": hash_arquivo,
                    "duracao": duracao,
                    "segundos": seg,
                    "transcricao": f"[ERRO NA TRANSCRIÇÃO: {str(e)}]",
                })
                pbar.update(1)

    # Gera laudo PDF se solicitado
    if gerar_pdf and arquivos_dados:
        try:
            caminho_pdf, hash_pdf = gerar_laudo_pdf(
                output_path, unidade, responsavel, model_choice, arquivos_dados
            )
            registrar_laudo()
            laudos_restantes = MAX_FREE_LAUDOS - laudos_gerados()

            msg = (
                f"Transcrição finalizada com sucesso!\n\n"
                f"Arquivo TXT: transcricoes.txt\n"
                f"Laudo PDF: {os.path.basename(caminho_pdf)}\n\n"
                f"Hash SHA-256 do laudo:\n{hash_pdf}"
            )
            if not tem_licenca() and laudos_restantes <= 0:
                msg += (
                    "\n\n⚠️ Você utilizou o laudo gratuito da versão de teste.\n"
                    "Para gerar novos laudos, adquira a licença anual do ApT."
                )
            messagebox.showinfo("Concluído!", msg)
        except Exception as e:
            messagebox.showerror("Erro ao gerar PDF", str(e))
    else:
        messagebox.showinfo("Concluído!", "Transcrição finalizada com sucesso!\n\nArquivo salvo: transcricoes.txt")


# ─────────────────────────────────────────────
# Interface gráfica
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("ApT — Áudio para Texto")
root.resizable(False, False)

# Ícone
os_type = platform.system()
icon_path = os.path.join("images", f"app_icon.{'ico' if os_type == 'Windows' else 'png'}")
if os.path.exists(icon_path):
    try:
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(False, icon_image)
    except tk.TclError as e:
        print(f"Erro ao carregar o ícone: {e}")

# Variáveis
input_folder = tk.StringVar()
output_folder = tk.StringVar()
model_var = tk.StringVar(value="large")
unidade_var = tk.StringVar()
responsavel_var = tk.StringVar()
gerar_pdf_var = tk.BooleanVar(value=True)

padding = {"padx": 10, "pady": 3}

# ── Identificação ──
frame_id = tk.LabelFrame(root, text="Identificação", padx=8, pady=6)
frame_id.pack(fill="x", padx=12, pady=(10, 4))

tk.Label(frame_id, text="Unidade:").grid(row=0, column=0, sticky="w")
tk.Entry(frame_id, textvariable=unidade_var, width=42).grid(row=0, column=1, padx=6, pady=2)

tk.Label(frame_id, text="Responsável:").grid(row=1, column=0, sticky="w")
tk.Entry(frame_id, textvariable=responsavel_var, width=42).grid(row=1, column=1, padx=6, pady=2)

# ── Pastas ──
frame_pastas = tk.LabelFrame(root, text="Pastas", padx=8, pady=6)
frame_pastas.pack(fill="x", padx=12, pady=4)

tk.Label(frame_pastas, text="Entrada:").grid(row=0, column=0, sticky="w")
tk.Entry(frame_pastas, textvariable=input_folder, width=36).grid(row=0, column=1, padx=6, pady=2)
tk.Button(frame_pastas, text="Selecionar", command=select_input_folder).grid(row=0, column=2)

tk.Label(frame_pastas, text="Saída:").grid(row=1, column=0, sticky="w")
tk.Entry(frame_pastas, textvariable=output_folder, width=36).grid(row=1, column=1, padx=6, pady=2)
tk.Button(frame_pastas, text="Selecionar", command=select_output_folder).grid(row=1, column=2)

# ── Modelo ──
frame_modelo = tk.LabelFrame(root, text="Modelo Whisper", padx=8, pady=6)
frame_modelo.pack(fill="x", padx=12, pady=4)

for i, (valor, texto) in enumerate([
    ("base", "base — rápido, menor precisão"),
    ("medium", "medium — equilibrado"),
    ("large", "large — melhor qualidade (recomendado) ⭐"),
]):
    tk.Radiobutton(frame_modelo, text=texto, variable=model_var, value=valor).grid(
        row=i, column=0, sticky="w"
    )

# ── Laudo PDF ──
frame_laudo = tk.LabelFrame(root, text="Laudo Forense", padx=8, pady=6)
frame_laudo.pack(fill="x", padx=12, pady=4)

laudos_usados = laudos_gerados()
if tem_licenca():
    status_licenca = "Licença ativa — laudos ilimitados"
    cor_status = "green"
else:
    restantes = MAX_FREE_LAUDOS - laudos_usados
    if restantes > 0:
        status_licenca = f"Versão gratuita — {restantes} laudo(s) disponível(is)"
        cor_status = "blue"
    else:
        status_licenca = "Versão gratuita — limite atingido. Adquira a licença."
        cor_status = "red"

tk.Checkbutton(
    frame_laudo, text="Gerar laudo PDF com cadeia de custódia (SHA-256)",
    variable=gerar_pdf_var
).pack(anchor="w")
tk.Label(frame_laudo, text=status_licenca, fg=cor_status, font=("Arial", 8)).pack(anchor="w")

# ── Progresso e botão ──
progress_label = tk.Label(root, text="Progresso: 0%")
progress_label.pack(**padding)

tk.Button(
    root, text="Iniciar Transcrição", bg="purple", fg="white",
    font=("Arial", 10, "bold"), padx=12, pady=6,
    command=start_transcription
).pack(pady=(4, 12))

root.mainloop()
