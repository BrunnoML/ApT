# core/pdf_report.py — Community Edition
#
# A geração de relatório PDF com cadeia de custódia está disponível
# apenas na versão instalada do ApT (via instalador oficial).
#
# Download: https://www.brunnoml.com.br/produtos/apt


def gerar_laudo_pdf(*args, **kwargs):
    raise RuntimeError(
        "A geração de relatório PDF está disponível apenas na versão "
        "instalada do ApT.\n\n"
        "Baixe o instalador em: https://www.brunnoml.com.br/produtos/apt"
    )
