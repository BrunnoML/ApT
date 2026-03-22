import hashlib
import os
import re
from datetime import datetime

from mutagen import File as MutagenFile


def calcular_hash(filepath: str) -> str:
    """Calcula o hash SHA-256 do arquivo antes de qualquer processamento."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def obter_duracao(filepath: str) -> str:
    """Retorna a duração do áudio formatada (HH:MM:SS ou MM:SS)."""
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


def segundos_totais(filepath: str) -> int:
    """Retorna duração em segundos inteiros para acumulação no relatório."""
    try:
        audio = MutagenFile(filepath)
        if audio is not None and hasattr(audio.info, "length"):
            return int(audio.info.length)
    except Exception:
        pass
    return 0


def extrair_data_arquivo(audio_path: str, filename: str) -> tuple[str, str]:
    """
    Extrai a data do arquivo de áudio com a melhor fonte disponível.
    Retorna (data_formatada, fonte_da_data).

    Prioridade:
      1. Nome do arquivo (WhatsApp PTT — data original da gravação)
      2. Metadados embutidos no arquivo de áudio (mutagen)
      3. mtime do sistema de arquivos (pode refletir transferência)
    """
    # 1. WhatsApp PTT: "WhatsApp Ptt YYYY-MM-DD at HH.MM.SS.ext"
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2})\.(\d{2})\.(\d{2})", filename)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d")
            hora = f"{m.group(2)}:{m.group(3)}:{m.group(4)}"
            return f"{dt.strftime('%d/%m/%Y')} {hora}", "nome do arquivo (WhatsApp)"
        except ValueError:
            pass

    # 2. Metadados embutidos via mutagen
    try:
        audio = MutagenFile(audio_path)
        if audio is not None and audio.tags:
            tags = audio.tags
            date_val = None

            # M4A / MP4
            if "©day" in tags:
                date_val = str(tags["©day"][0])
            # OGG / FLAC (Vorbis Comments)
            elif "date" in tags:
                v = tags["date"]
                date_val = str(v[0] if isinstance(v, list) else v)
            elif "DATE" in tags:
                v = tags["DATE"]
                date_val = str(v[0] if isinstance(v, list) else v)
            # MP3 ID3
            elif "TDRC" in tags:
                date_val = str(tags["TDRC"])
            elif "TYER" in tags:
                date_val = str(tags["TYER"])
            # WAV RIFF
            elif "ICRD" in tags:
                date_val = str(tags["ICRD"])

            if date_val and len(date_val) >= 4:
                for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y"):
                    try:
                        dt = datetime.strptime(date_val[:len(fmt)], fmt)
                        return dt.strftime("%d/%m/%Y"), "metadados do arquivo de áudio"
                    except ValueError:
                        continue
    except Exception:
        pass

    # 3. mtime do sistema de arquivos (fallback)
    try:
        mtime = os.path.getmtime(audio_path)
        data = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M:%S")
        return data, "data do sistema de arquivos (pode refletir transferência para o PC)"
    except Exception:
        pass

    return "não disponível", "desconhecida"


def obter_tamanho(filepath: str) -> str:
    """Retorna o tamanho do arquivo em formato legível (bytes e KB/MB)."""
    try:
        size = os.path.getsize(filepath)
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB ({size:,} bytes)"
        else:
            return f"{size / (1024 * 1024):.2f} MB ({size:,} bytes)"
    except Exception:
        return "não disponível"


def formatar_duracao_total(segundos: int) -> str:
    """Formata total de segundos em HH:MM:SS ou MM:SS."""
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"
    return f"{minutos:02d}:{segs:02d}"
