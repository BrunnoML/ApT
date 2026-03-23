"""
Lógica de transcrição desacoplada da UI.

Roda em thread separada e comunica o progresso via callbacks,
garantindo que a interface nunca trave durante o processamento.

Callbacks esperados:
  progress_callback(atual: int, total: int, nome: str) -> None
  done_callback(msg: str, pdf_path: str | None, hash_pdf: str | None) -> None
  error_callback(msg: str) -> None
"""
import concurrent.futures
import io
import os
import sys
from datetime import datetime
from typing import Callable

import whisper

from core.audio_utils import calcular_hash, obter_duracao, obter_tamanho, segundos_totais, extrair_data_arquivo
from core.pdf_report import gerar_laudo_pdf
from licensing.license_manager import (
    tem_licenca_ativa,
    pode_transcrever,
    registrar_segundos,
    segundos_restantes_gratis,
    MAX_FREE_SEGUNDOS,
)

EXTENSOES_SUPORTADAS = (
    ".mp3", ".m4a", ".m4b", ".ogg", ".oga", ".opus",
    ".wav", ".mp4", ".wma", ".flac", ".aac",
    ".amr", ".awb", ".3gp",
)
TIMEOUT_TRANSCRICAO = 120       # segundos — arquivo legível (mutagen ok)
TIMEOUT_ILEGIVEL    = 30        # segundos — arquivo que mutagen não reconheceu


def transcrever_arquivos(
    input_path: str,
    output_path: str,
    model_name: str,
    gerar_pdf: bool,
    unidade: str,
    responsavel: str,
    progress_callback: Callable[[int, int, str], None],
    done_callback: Callable[[str, str | None, str | None], None],
    error_callback: Callable[[str], None],
    logo_path: str | None = None,
) -> None:
    """
    Transcreve todos os áudios de input_path e salva em output_path.
    Deve ser chamada em uma thread daemon, nunca na thread da UI.
    Respeita os limites da versão gratuita (30 min de áudio acumulados).
    """
    try:
        arquivos = sorted([
            f for f in os.listdir(input_path)
            if f.lower().endswith(EXTENSOES_SUPORTADAS)
        ])
    except Exception as e:
        error_callback(f"Erro ao listar pasta de entrada: {e}")
        return

    total = len(arquivos)
    if total == 0:
        error_callback("Nenhum arquivo de áudio encontrado na pasta selecionada.")
        return

    # Verifica limite de áudio antes de carregar o modelo
    licenciado = tem_licenca_ativa()
    if not licenciado and segundos_restantes_gratis() <= 0:
        error_callback(
            f"Limite da versão gratuita atingido: {MAX_FREE_SEGUNDOS // 60} minutos de áudio já processados.\n\n"
            "Adquira a licença para processamento ilimitado."
        )
        return

    tamanhos = {"tiny": "39 MB", "base": "74 MB", "small": "244 MB", "medium": "769 MB", "large": "1,5 GB"}
    tam = tamanhos.get(model_name, "")
    progress_callback(0, total, f"Carregando modelo '{model_name}' {tam}… (1ª execução: faz download automático)")
    # sys.stdout/stderr são None em apps PyInstaller sem console.
    # O tqdm do Whisper trava ao tentar escrever o progresso do download.
    _stdout, _stderr = sys.stdout, sys.stderr
    if sys.stdout is None:
        sys.stdout = io.StringIO()
    if sys.stderr is None:
        sys.stderr = io.StringIO()
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        error_callback(f"Erro ao carregar modelo Whisper '{model_name}': {e}")
        return
    finally:
        sys.stdout, sys.stderr = _stdout, _stderr

    output_file = os.path.join(output_path, "transcricoes.txt")
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("")
    except Exception as e:
        error_callback(f"Erro ao criar arquivo de saída: {e}")
        return

    arquivos_dados = []
    pulados = []

    for idx, filename in enumerate(arquivos, 1):
        audio_path = os.path.normpath(os.path.join(input_path, filename))
        seg = segundos_totais(audio_path)

        # Verifica limite de áudio para usuários sem licença
        if not licenciado and not pode_transcrever(seg):
            pulados.append(filename)
            progress_callback(idx, total, f"[LIMITE] {filename}")
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"Arquivo : {filename}\n")
                f.write(f"Status  : PULADO — limite de áudio da versão gratuita atingido\n")
                f.write(f"{'=' * 60}\n")
            continue

        progress_callback(idx, total, filename)

        hash_arquivo = calcular_hash(audio_path)
        duracao = obter_duracao(audio_path)
        tamanho = obter_tamanho(audio_path)
        data_arquivo, fonte_data = extrair_data_arquivo(audio_path, filename)

        # Se mutagen não leu metadados, o arquivo provavelmente está corrompido:
        # usa timeout curto para não travar no FFmpeg.
        timeout = TIMEOUT_ILEGIVEL if duracao == "Indisponível" else TIMEOUT_TRANSCRICAO
        try:
            _ex = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            _fut = _ex.submit(model.transcribe, audio_path)
            _ex.shutdown(wait=False)  # não bloqueia se a thread travar
            result = _fut.result(timeout=timeout)
            texto = result["text"]
        except concurrent.futures.TimeoutError:
            texto = "[ARQUIVO ILEGÍVEL: o processamento excedeu o tempo limite — arquivo possivelmente corrompido ou incompleto]"
        except Exception as e:
            msg = str(e)
            if "Failed to load audio" in msg or "Invalid data" in msg or "Error opening" in msg:
                texto = "[ARQUIVO ILEGÍVEL: não foi possível decodificar o áudio — arquivo corrompido, incompleto ou em formato inválido]"
            else:
                texto = f"[ERRO NA TRANSCRIÇÃO: {msg}]"

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"Arquivo : {filename}\n")
            f.write(f"Data    : {data_arquivo}\n")
            f.write(f"Hash    : {hash_arquivo}\n")
            f.write(f"Duração : {duracao}\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"{texto}\n")

        arquivos_dados.append({
            "nome": filename,
            "data": data_arquivo,
            "fonte_data": fonte_data,
            "tamanho": tamanho,
            "hash": hash_arquivo,
            "duracao": duracao,
            "segundos": seg,
            "transcricao": texto,
        })

        # Registra segundos consumidos apenas para usuários sem licença
        if not licenciado:
            registrar_segundos(seg)

    # Compõe mensagem final
    aviso_pulados = ""
    if pulados:
        aviso_pulados = (
            f"\n\n⚠️ {len(pulados)} arquivo(s) não processado(s) por limite da versão gratuita:\n"
            + "\n".join(f"  • {f}" for f in pulados)
            + "\n\nAdquira a licença para processar sem limites."
        )

    # Gera laudo PDF se solicitado
    if gerar_pdf and arquivos_dados:
        try:
            caminho_pdf, hash_pdf = gerar_laudo_pdf(
                output_path, unidade, responsavel, model_name, arquivos_dados,
                logo_path=logo_path,
            )
            # Registra hash do PDF ao final de transcricoes.txt para consulta futura
            agora_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"INTEGRIDADE DO RELATÓRIO PDF\n")
                f.write(f"{'=' * 60}\n")
                f.write(f"Arquivo     : {os.path.basename(caminho_pdf)}\n")
                f.write(f"Hash SHA-256: {hash_pdf}\n")
                f.write(f"Gerado em   : {agora_str}\n")
                f.write(f"{'=' * 60}\n")
            msg = (
                f"Transcrição finalizada!\n\n"
                f"Arquivos gerados:\n"
                f"  • transcricoes.txt\n"
                f"  • {os.path.basename(caminho_pdf)}\n\n"
                f"Hash SHA-256 do relatório:\n{hash_pdf}"
                + aviso_pulados
            )
            done_callback(msg, caminho_pdf, hash_pdf)
        except Exception as e:
            error_callback(f"Erro ao gerar laudo PDF: {e}")
    else:
        done_callback(
            "Transcrição finalizada!\n\nArquivo salvo: transcricoes.txt" + aviso_pulados,
            None,
            None,
        )
