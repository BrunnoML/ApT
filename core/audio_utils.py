import hashlib
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


def formatar_duracao_total(segundos: int) -> str:
    """Formata total de segundos em HH:MM:SS ou MM:SS."""
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"
    return f"{minutos:02d}:{segs:02d}"
