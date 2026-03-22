"""
Identificador único de máquina para vinculação de licença.

Usa MAC address + hostname para gerar um hash estável.
Não requer privilégios de administrador.
"""
import hashlib
import platform
import uuid


def get_machine_id() -> str:
    """Retorna hash SHA-256 completo da máquina (64 chars hex)."""
    mac = str(uuid.getnode())
    hostname = platform.node()
    raw = f"{mac}:{hostname}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get_machine_id_display() -> str:
    """Retorna código legível para exibir na UI e enviar na solicitação.
    Formato: XXXX-XXXX-XXXX (12 chars do hash, maiúsculas)
    """
    full = get_machine_id()
    s = full[:12].upper()
    return f"{s[:4]}-{s[4:8]}-{s[8:12]}"
