"""
Gerenciamento do estado de licença local.

O arquivo .apt_license é um JSON salvo no mesmo diretório do executável.
Ele controla:
  - Contador de laudos gerados na versão gratuita
  - Caminho do arquivo .apt_lic ativo (licença premium)

A emissão de licenças é feita externamente (repositório privado).
Este módulo apenas lê, valida e persiste o estado local.
"""
import json
import os
import sys

from licensing.license_validator import verificar_licenca

MAX_FREE_LAUDOS = 1

# Localização do arquivo de estado — junto ao executável (PyInstaller) ou ao script
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__ + "/../../"))

LICENSE_FILE = os.path.join(_BASE, ".apt_license")


def _ler() -> dict:
    if not os.path.exists(LICENSE_FILE):
        return {"laudos": 0, "lic_path": None}
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"laudos": 0, "lic_path": None}
            return data
    except Exception:
        return {"laudos": 0, "lic_path": None}


def _salvar(data: dict) -> None:
    with open(LICENSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def laudos_gerados() -> int:
    return _ler().get("laudos", 0)


def registrar_laudo() -> None:
    data = _ler()
    data["laudos"] = data.get("laudos", 0) + 1
    _salvar(data)


def carregar_licenca_ativa() -> dict | None:
    """
    Lê o .apt_lic salvo e valida a assinatura Ed25519.
    Retorna os dados da licença ou None se inválida/ausente.
    """
    lic_path = _ler().get("lic_path")
    if not lic_path or not os.path.exists(lic_path):
        return None
    valido, _msg, dados = verificar_licenca(lic_path)
    return dados if valido else None


def tem_licenca_ativa() -> bool:
    return carregar_licenca_ativa() is not None


def pode_gerar_laudo() -> bool:
    return tem_licenca_ativa() or laudos_gerados() < MAX_FREE_LAUDOS


def get_status_licenca() -> dict:
    """
    Retorna dict com:
      valida: bool
      mensagem: str  (para exibir na UI)
      dados: dict    (conteúdo da licença, ou {})
    """
    lic_path = _ler().get("lic_path")
    if not lic_path or not os.path.exists(lic_path):
        restantes = MAX_FREE_LAUDOS - laudos_gerados()
        if restantes > 0:
            return {
                "valida": False,
                "mensagem": f"Versão gratuita — {restantes} laudo(s) disponível(is)",
                "dados": {},
            }
        return {
            "valida": False,
            "mensagem": "Versão gratuita — limite atingido. Adquira a licença.",
            "dados": {},
        }

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


def ativar_licenca(caminho_lic: str) -> tuple[bool, str]:
    """
    Tenta ativar um arquivo .apt_lic.
    Retorna (sucesso, mensagem).
    """
    if not os.path.exists(caminho_lic):
        return False, "Arquivo não encontrado."

    valido, msg, dados = verificar_licenca(caminho_lic)
    if not valido:
        return False, msg

    data = _ler()
    data["lic_path"] = caminho_lic
    _salvar(data)
    return True, f"Licença ativada: {dados.get('unidade', '')} | válida até {dados.get('expiry', '')}"
