"""
Gerenciamento do estado de licença local.

O arquivo .apt_license é um JSON salvo no mesmo diretório do executável.
Ele controla:
  - Contador de laudos gerados na versão gratuita
  - Total de segundos de áudio processados na versão gratuita
  - Caminho do arquivo .apt_lic ativo (licença premium)

A emissão de licenças é feita externamente (repositório privado).
Este módulo apenas lê, valida e persiste o estado local.
"""
import json
import os
import sys

from licensing.license_validator import verificar_licenca

MAX_FREE_LAUDOS = 1
MAX_FREE_SEGUNDOS = 1800  # 30 minutos

# Localização do arquivo de estado — junto ao executável (PyInstaller) ou ao script
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__ + "/../../"))

LICENSE_FILE = os.path.join(_BASE, ".apt_license")

_DEFAULT = {"laudos": 0, "segundos": 0, "lic_path": None}


def _ler() -> dict:
    if not os.path.exists(LICENSE_FILE):
        return dict(_DEFAULT)
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return dict(_DEFAULT)
            # Garante que campos novos existam em arquivos antigos
            return {**_DEFAULT, **data}
    except Exception:
        return dict(_DEFAULT)


def _salvar(data: dict) -> None:
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Laudos ──────────────────────────────────────────────────────────────────

def laudos_gerados() -> int:
    return _ler().get("laudos", 0)


def registrar_laudo() -> None:
    data = _ler()
    data["laudos"] = data.get("laudos", 0) + 1
    _salvar(data)


def pode_gerar_laudo() -> bool:
    return tem_licenca_ativa() or laudos_gerados() < MAX_FREE_LAUDOS


# ── Áudio ────────────────────────────────────────────────────────────────────

def segundos_processados() -> int:
    return _ler().get("segundos", 0)


def registrar_segundos(n: int) -> None:
    """Acumula os segundos de áudio processado (apenas para usuários sem licença)."""
    data = _ler()
    data["segundos"] = data.get("segundos", 0) + max(0, n)
    _salvar(data)


def segundos_restantes_gratis() -> int:
    return max(0, MAX_FREE_SEGUNDOS - segundos_processados())


def pode_transcrever(seg_arquivo: int = 0) -> bool:
    """True se o usuário pode processar este arquivo (com ou sem licença)."""
    if tem_licenca_ativa():
        return True
    return segundos_processados() + seg_arquivo <= MAX_FREE_SEGUNDOS


# ── Licença ──────────────────────────────────────────────────────────────────

def carregar_licenca_ativa() -> dict | None:
    lic_path = _ler().get("lic_path")
    if not lic_path or not os.path.exists(lic_path):
        return None
    valido, _msg, dados = verificar_licenca(lic_path)
    return dados if valido else None


def tem_licenca_ativa() -> bool:
    return carregar_licenca_ativa() is not None


def get_status_licenca() -> dict:
    """
    Retorna dict com:
      valida: bool
      mensagem: str   (para exibir na UI)
      dados: dict     (conteúdo da licença, ou {})
    """
    lic_path = _ler().get("lic_path")

    if lic_path and os.path.exists(lic_path):
        valido, msg, dados = verificar_licenca(lic_path)
        if valido:
            return {
                "valida": True,
                "mensagem": f"Licença ativa — {dados.get('unidade', '')} | válida até {dados.get('expiry', '')}",
                "dados": dados,
            }
        return {
            "valida": False,
            "mensagem": f"Licença inválida: {msg}",
            "dados": {},
        }

    # Versão gratuita — calcula o que ainda está disponível
    laudos_rest = MAX_FREE_LAUDOS - laudos_gerados()
    seg_rest = segundos_restantes_gratis()
    min_rest = seg_rest // 60
    seg_rest_mod = seg_rest % 60

    if laudos_rest <= 0 and seg_rest <= 0:
        mensagem = "Licença Gratuita — limites atingidos. Adquira a licença."
    elif laudos_rest <= 0:
        mensagem = f"Licença Gratuita — laudo já utilizado | {min_rest:02d}:{seg_rest_mod:02d} de áudio restantes"
    elif seg_rest <= 0:
        mensagem = f"Licença Gratuita — limite de áudio atingido | {laudos_rest} laudo(s) disponível(is)"
    else:
        mensagem = (
            f"Licença Gratuita — {laudos_rest} laudo(s) | "
            f"{min_rest:02d}:{seg_rest_mod:02d} de áudio restantes"
        )

    return {"valida": False, "mensagem": mensagem, "dados": {}}


def ativar_licenca(caminho_lic: str) -> tuple[bool, str]:
    if not os.path.exists(caminho_lic):
        return False, "Arquivo não encontrado."

    valido, msg, dados = verificar_licenca(caminho_lic)
    if not valido:
        return False, msg

    data = _ler()
    data["lic_path"] = caminho_lic
    _salvar(data)
    return True, f"Licença ativada: {dados.get('unidade', '')} | válida até {dados.get('expiry', '')}"
