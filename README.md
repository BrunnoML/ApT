<h1 align="center">🎙️ ApT - Áudio para Texto</h1>

<p align="center">
<strong>Software de transcrição de áudio licenciado para uso local.</strong>
</p>

<p align="center">
Transforme horas de áudio em texto pesquisável em minutos — ideal para profissionais da área jurídica, investigativa e pericial que precisam ganhar produtividade, organizar evidências e gerar laudos prontos para o processo.
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-modelo-de-licenciamento">Licenciamento</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-licenciamento">Código Aberto</a>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=Apache-2.0&color=49AA26&labelColor=000000">
</p>

<p align="center">
  <strong>⚖️ Licenciamento duplo:</strong> código comunitário sob Apache 2.0 &nbsp;|&nbsp; funcionalidades premium regidas por <a href="EULA.md">EULA próprio</a>
</p>

---

<p align="center">
  <img alt="ApT" src="/images/preview.png" width="500px">
</p>

<p align="center">
  🔒 <strong>Processamento 100% local</strong> — seus arquivos de áudio nunca saem do seu dispositivo.
</p>

---

## ⚖️ Sobre o ApT

O **ApT (Áudio para Texto)** é uma aplicação desktop que utiliza inteligência artificial para transcrever arquivos de áudio em texto de forma automatizada, com geração de **laudo PDF forense** e elementos voltados à documentação da cadeia de custódia do material processado.

Desenvolvido para eliminar o gargalo mais comum na análise de áudios:

- Substituir horas de escuta manual por texto pesquisável em minutos
- Localizar trechos relevantes por palavra-chave, sem ouvir arquivo por arquivo
- Gerar laudos prontos para juntada ao processo, com hash SHA-256 e documentação técnica do material processado

---

## 🎯 Público-alvo

O ApT é especialmente útil para:

- Delegados e investigadores
- Advogados e defensores públicos
- Promotores e magistrados
- Peritos e analistas
- Estudantes e pesquisadores

---

## ✨ Funcionalidades

- Interface gráfica moderna com tema escuro
- Transcrição automática de áudios usando IA (100% local)
- Processamento de múltiplos arquivos em lote
- Seleção de modelos Whisper (`base`, `medium`, `large`)
- Exportação de transcrições em `.txt`
- Geração de **laudo PDF forense** com cadeia de custódia (hash SHA-256)
- Organização por pastas de entrada e saída

---

## 📄 Modelo de Licenciamento

O ApT é disponibilizado sob **modelo de licenciamento de software**. O Autor concede ao usuário o direito de uso da aplicação — não há prestação de serviço, processamento remoto ou dependência de servidores externos.

A versão comunitária inclui funcionalidades limitadas. Funcionalidades adicionais são habilitadas mediante **licença de uso** adquirida junto ao Autor.

### 🟢 Versão Gratuita
- Transcrição de até **30 minutos** de áudio (acumulado)
- Geração de até **1 laudo PDF** forense
- Uso local, sem envio de dados para servidores externos

### 🔵 Versão Licenciada (Profissional)
- Transcrição e geração de laudos PDF ilimitados
- Cadeia de custódia completa em cada laudo
- Recursos adicionais conforme o plano adquirido
- Acesso a atualizações e suporte associado à licença, durante sua vigência

👉 **Consulte as modalidades de licenciamento de uso disponíveis:**

🔗 **https://www.brunnoml.com.br/apt**

---

## 🛠️ Instalação

### 👤 Usuário final (recomendado)

> Em breve será disponibilizada uma versão instalável.

O objetivo é permitir que o usuário:

- baixe o instalador
- execute com duplo clique
- utilize sem necessidade de terminal

---

### 💻 Modo desenvolvedor (instalação manual)

1. Clone o repositório:

```bash
git clone https://github.com/BrunnoML/ApT.git
cd apt
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative:

**Windows**

```
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

3. Instale dependências:

```bash
pip install --upgrade pip
pip install setuptools==69.5.1 wheel
pip install --no-build-isolation -r requirements.txt
```

4. Execute:

```bash
python main.py
```

---

## 🔈 Configuração do FFmpeg

O FFmpeg é necessário para o processamento dos áudios.

Atualmente, a instalação é manual, conforme descrito abaixo.

> ⚠️ Em versões futuras, o FFmpeg será incorporado automaticamente ao sistema.

### Download:

[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

Baixe:

```
ffmpeg-release-essentials.zip
```

Configure conforme instruções padrão do Windows.

---

## 🚀 Tecnologias

- Python 3.12
- Whisper (OpenAI) — transcrição de áudio local
- CustomTkinter — interface moderna
- ReportLab — geração de laudo PDF
- Cryptography — verificação de licença (Ed25519)
- FFmpeg — processamento de áudio

---

## 🔐 Licenciamento

O projeto possui duas camadas de licenciamento:

### 📂 Código-fonte (comunitário)

Disponível sob a **Apache License 2.0**, conforme definido no arquivo [`LICENSE`](LICENSE).

### 💼 Funcionalidades premium

O acesso às funcionalidades avançadas exige licença de uso válida, adquirida junto ao Autor. A disponibilidade do código-fonte não implica acesso automático às funcionalidades licenciadas.

Documentos relevantes:

- [`TERMS.md`](TERMS.md) — Termos de uso
- [`EULA.md`](EULA.md) — Contrato de licença de usuário final (EULA)
- [`PRICING.md`](PRICING.md) — Modalidades de licenciamento disponíveis

---

## 📈 Evolução do Projeto

O ApT está em evolução contínua, com melhorias planejadas:

- Instalador simplificado (sem necessidade de terminal)
- FFmpeg incorporado automaticamente
- Identificação de interlocutores (diarização)
- Detecção de palavras-chave configurável
- Integração com outras ferramentas forenses

---

## ☕ Autor

Desenvolvido por **Brunno ML**

🔗 [https://www.brunnoml.com.br](https://www.brunnoml.com.br)

---

## ⭐ Contribuição

Sugestões, melhorias e feedbacks são bem-vindos!

Se este projeto foi útil para você, considere dar uma ⭐ no repositório.
