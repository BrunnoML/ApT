"""
Validador de licença Ed25519 — lado do cliente.

APENAS a chave pública está aqui.
A chave privada (para assinar/emitir licenças) nunca entra neste repositório.

Formato do arquivo .apt_lic (JSON):
{
  "version": 1,
  "unidade": "DEAM-SP-001",
  "plan": "unit",
  "expiry": "2027-03-21",
  "issued": "2026-03-21",
  "features": ["pdf_unlimited", "logo_custom"],
  "sig": "<base64url-assinatura-ed25519>"
}

A assinatura cobre o conteúdo canônico: JSON com todas as chaves exceto "sig",
ordenado alfabeticamente, sem espaços extras, encoding UTF-8.
"""
import base64
import json
import os
from datetime import date

# ─────────────────────────────────────────────────────────────
# CHAVE PÚBLICA Ed25519 (gerada com cryptography, nunca privada)
# Substitua pelo valor real após gerar o par de chaves:
#   python scripts/gerar_chaves.py   (repositório privado)
# ─────────────────────────────────────────────────────────────
_PUBLIC_KEY_PEM = b"""-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEADmSnlqZqSrvKPw+WF46SJCsXvSzT/E0bP+KwZHwezZ4=
-----END PUBLIC KEY-----"""

_CHAVE_PUBLICA_CONFIGURADA = b"PLACEHOLDER" not in _PUBLIC_KEY_PEM


def _payload_canonico(dados: dict) -> bytes:
    """Serializa o payload sem o campo 'sig', ordenado, sem espaços."""
    payload = {k: v for k, v in dados.items() if k != "sig"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def verificar_licenca(caminho_lic: str) -> tuple[bool, str, dict]:
    """
    Verifica a assinatura Ed25519 do arquivo .apt_lic e a validade da data.

    Retorna (valido: bool, mensagem: str, dados: dict).
    Em caso de erro retorna (False, motivo, {}).
    """
    # Guarda de emergência: se a chave pública não foi configurada ainda,
    # avisar o desenvolvedor sem travar o app.
    if not _CHAVE_PUBLICA_CONFIGURADA:
        return False, "Chave pública não configurada. Execute scripts/gerar_chaves.py.", {}

    if not os.path.exists(caminho_lic):
        return False, "Arquivo de licença não encontrado.", {}

    try:
        with open(caminho_lic, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception as e:
        return False, f"Erro ao ler arquivo de licença: {e}", {}

    # Campos obrigatórios
    campos = {"version", "unidade", "plan", "expiry", "issued", "features", "sig"}
    ausentes = campos - set(dados.keys())
    if ausentes:
        return False, f"Campos ausentes no arquivo de licença: {ausentes}", {}

    # Vinculação de máquina — se o campo existir na licença, deve coincidir
    if "machine_id" in dados:
        from licensing.machine_id import get_machine_id_display
        current = get_machine_id_display().replace("-", "").lower()
        if dados["machine_id"] != current:
            return False, "Licença vinculada a outra máquina. Solicite uma nova licença.", {}

    sig_b64 = dados.get("sig", "")

    try:
        sig_bytes = base64.urlsafe_b64decode(sig_b64 + "==")
    except Exception:
        return False, "Assinatura com formato inválido (base64url esperado).", {}

    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.exceptions import InvalidSignature

        chave_publica: Ed25519PublicKey = load_pem_public_key(_PUBLIC_KEY_PEM)
        chave_publica.verify(sig_bytes, _payload_canonico(dados))
    except InvalidSignature:
        return False, "Assinatura inválida. Licença não reconhecida.", {}
    except Exception as e:
        return False, f"Erro na verificação criptográfica: {e}", {}

    # Verifica expiração
    try:
        expiry = date.fromisoformat(dados["expiry"])
    except ValueError:
        return False, "Data de expiração com formato inválido (YYYY-MM-DD esperado).", {}

    if date.today() > expiry:
        return False, f"Licença expirada em {dados['expiry']}.", {}

    return True, "Licença válida.", dados
