<h1 align="center">🎙️ ApT — Áudio para Texto</h1>

<p align="center">
<strong>Software de transcrição de áudio licenciado para uso local.</strong>
</p>

<p align="center">
Transforme horas de áudio em texto pesquisável em minutos — ideal para profissionais da área jurídica, investigativa e pericial que precisam ganhar produtividade, organizar evidências e gerar relatórios prontos para o processo.
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-licenciamento">Licenciamento</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-licença-do-código">Código Aberto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  <a href="https://github.com/BrunnoML/ApT/releases/tag/v1.1.0">
    <img alt="Release" src="https://img.shields.io/badge/release-v1.1.0-6d28d9?labelColor=000000">
  </a>
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=Apache-2.0&color=49AA26&labelColor=000000">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-blue?labelColor=000000">
</p>

<p align="center">
  <strong>⚖️ Licenciamento duplo:</strong> código comunitário sob Apache 2.0 &nbsp;|&nbsp; funcionalidades premium regidas por <a href="EULA.md">EULA próprio</a>
</p>

---

<p align="center">
  🔒 <strong>Processamento 100% local</strong> — seus arquivos de áudio nunca saem do seu dispositivo.
</p>

---

## ⚖️ Sobre o ApT

O **ApT (Áudio para Texto)** é uma aplicação desktop que utiliza inteligência artificial para transcrever arquivos de áudio em texto de forma automatizada, com geração de **relatório técnico em PDF** e documentação da cadeia de custódia do material processado — em conformidade com a Lei 13.964/2019 (Pacote Anticrime).

Desenvolvido para eliminar o gargalo mais comum na análise de áudios:

- Substituir horas de escuta manual por texto pesquisável em minutos
- Localizar trechos relevantes por palavra-chave, sem ouvir arquivo por arquivo
- Gerar relatórios prontos para juntada ao processo, com hash SHA-256 de cada arquivo processado

---

## 🎯 Público-alvo

- Delegados e investigadores
- Escrivães e agentes de polícia
- Advogados e defensores públicos
- Promotores e magistrados
- Peritos e analistas
- Estudantes e pesquisadores

---

## ✨ Funcionalidades

- Interface gráfica moderna com tema escuro
- Transcrição automática de áudios com IA (100% local, sem internet)
- Processamento em lote — selecione a pasta e processe todos os áudios de uma vez
- Modelos Whisper: `base` ⭐ recomendado · `medium` · `large` para áudios difíceis
- Exportação de transcrições em `.txt` com hash SHA-256 de cada arquivo
- Geração de **relatório técnico em PDF** com cadeia de custódia (Lei 13.964/2019)
- FFmpeg embutido — sem necessidade de instalação adicional

---

## 🎵 Formatos de áudio suportados

| Extensão | Origem principal |
|----------|-----------------|
| `.mp3`   | Formato universal |
| `.m4a`   | iOS, Android, Signal, WhatsApp (versões antigas) |
| `.m4b`   | iOS Voice Memos |
| `.ogg` / `.oga` | Telegram |
| `.opus`  | WhatsApp (atual), Signal, Viber |
| `.wav`   | Gravações diversas |
| `.mp4`   | Instagram, Messenger (pista de áudio) |
| `.aac`   | Facebook, Android |
| `.flac`  | Gravações de alta qualidade |
| `.wma`   | Dispositivos Windows antigos |
| `.amr`   | Android (WhatsApp versões antigas, gravadores) |
| `.awb`   | AMR Wideband — variante de `.amr` |
| `.3gp`   | Gravador nativo Android, extrações UFED/Cellebrite |

> Todos os formatos são processados via **FFmpeg embutido** — nenhuma instalação adicional necessária.

---

## 📄 Licenciamento

| Licença | Limite |
|---------|--------|
| **Gratuita** | Até 30 min de áudio acumulado + 1 relatório PDF |
| **Mensal** | Transcrição e relatórios ilimitados por 30 dias |
| **Anual** | Transcrição e relatórios ilimitados por 12 meses _(melhor custo-benefício)_ |

👉 **Solicite a licença:**

🔗 **[brunnoml.com.br/produtos/apt](https://www.brunnoml.com.br/produtos/apt)**

---

## 🛠️ Instalação

### 👤 Usuário final (recomendado)

1. Baixe o instalador: **[ApT-Setup-v1.1.0.exe](https://github.com/BrunnoML/ApT/releases/download/v1.1.0/ApT-Setup-v1.1.0.exe)**
2. Execute o instalador e siga os passos
3. Abra o ApT pelo Menu Iniciar

> **Modelos Whisper** são baixados automaticamente na primeira execução de cada modelo:
> `base` ≈ 74 MB · `medium` ≈ 769 MB · `large` ≈ 1,5 GB

**Requisitos:** Windows 10 / 11 (64-bit)

---

### 💻 Modo desenvolvedor (instalação manual)

1. Clone o repositório:

```bash
git clone https://github.com/BrunnoML/ApT.git
cd apt
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install --upgrade pip
pip install setuptools==69.5.1 wheel
pip install --no-build-isolation -r requirements.txt
```

4. Execute:

```bash
python main.py
```

> Para empacotar o executável: `pyinstaller apt.spec`

---

## 🚀 Tecnologias

- **Python 3.12**
- **Whisper (OpenAI)** — transcrição de áudio local
- **CustomTkinter** — interface moderna
- **ReportLab** — geração de relatório PDF
- **Cryptography (Ed25519)** — verificação de licença
- **FFmpeg** — processamento de áudio (embutido)

---

## 📈 Evolução planejada

- Identificação de interlocutores (diarização)
- Detecção de palavras-chave configurável
- Integração com outras ferramentas forenses

---

## 🔐 Licença do código

### 📂 Código-fonte (comunitário)

Disponível sob a **Apache License 2.0**, conforme definido no arquivo [`LICENSE`](LICENSE).

### 💼 Funcionalidades premium

O acesso às funcionalidades avançadas exige licença de uso válida, adquirida junto ao Autor. A disponibilidade do código-fonte não implica acesso automático às funcionalidades licenciadas.

Documentos relevantes:

- [`TERMS.md`](TERMS.md) — Termos de uso
- [`EULA.md`](EULA.md) — Contrato de licença de usuário final
- [`PRICING.md`](PRICING.md) — Modalidades de licenciamento

---

## ☕ Autor

Desenvolvido por **Brunno ML**

🔗 [brunnoml.com.br](https://www.brunnoml.com.br)

---

## ⭐ Contribuição

Sugestões, melhorias e feedbacks são bem-vindos!

Se este projeto foi útil para você, considere dar uma ⭐ no repositório.
