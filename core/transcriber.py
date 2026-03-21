"""
Lógica de transcrição desacoplada da UI.

Roda em thread separada e comunica o progresso via callbacks,
garantindo que a interface nunca trave durante o processamento.

Callbacks esperados:
  progress_callback(atual: int, total: int, nome: str) -> None
  done_callback(msg: str, pdf_path: str | None, hash_pdf: str | None) -> None
  error_callback(msg: str) -> None
"""
import os
from typing import Callable

import whisper

from core.audio_utils import calcular_hash, obter_duracao, segundos_totais
from core.pdf_report import gerar_laudo_pdf
from licensing.license_manager import (
    tem_licenca_ativa,
    pode_transcrever,
    registrar_segundos,
    segundos_restantes_gratis,
    MAX_FREE_SEGUNDOS,
)

EXTENSOES_SUPORTADAS = (".m4a", ".ogg", ".wav", ".mp3", ".mp4", ".wma", ".flac", ".aac")


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

    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        error_callback(f"Erro ao carregar modelo Whisper '{model_name}': {e}")
        return

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

        try:
            result = model.transcribe(audio_path)
            texto = result["text"]
        except Exception as e:
            texto = f"[ERRO NA TRANSCRIÇÃO: {e}]"

        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 60}\n")
            f.write(f"Arquivo : {filename}\n")
            f.write(f"Hash    : {hash_arquivo}\n")
            f.write(f"Duração : {duracao}\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"{texto}\n")

        arquivos_dados.append({
            "nome": filename,
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
                output_path, unidade, responsavel, model_name, arquivos_dados
            )
            msg = (
                f"Transcrição finalizada!\n\n"
                f"Arquivo TXT: transcricoes.txt\n"
                f"Laudo PDF: {os.path.basename(caminho_pdf)}\n\n"
                f"Hash SHA-256 do laudo:\n{hash_pdf}"
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
