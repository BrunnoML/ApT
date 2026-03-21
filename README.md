<h1 align="center">🎙️ ApT - Áudio para Texto</h1>

<p align="center">
<strong>Transforme horas de áudio em texto pesquisável em minutos.</strong>
</p>

<p align="center">
Ideal para profissionais da área jurídica, investigativa e pericial que precisam ganhar produtividade, organizar evidências e gerar laudos prontos para o processo.
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-modalidades-de-uso">Modalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-licenciamento">Licenciamento</a>
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

O **ApT (Áudio para Texto)** é uma aplicação desktop que utiliza inteligência artificial para transcrever arquivos de áudio em texto de forma automatizada, com geração de **laudo PDF forense** e preservação da cadeia de custódia conforme a Lei 13.964/2019.

Desenvolvido para eliminar o gargalo mais comum na análise de áudios:

- Substituir horas de escuta manual por texto pesquisável em minutos
- Localizar trechos relevantes por palavra-chave, sem ouvir arquivo por arquivo
- Gerar laudos prontos para juntada ao processo, com hash SHA-256 e conformidade legal

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

## 🔐 Modalidades de Uso

O ApT segue um modelo **freemium**:

### 🟢 Versão Gratuita
- Transcrição de áudio para texto
- Uso local da aplicação
- Geração limitada de laudos PDF

### 🔵 Versão Licenciada (Profissional)
- Geração ilimitada de laudos PDF forenses
- Cadeia de custódia completa em cada laudo
- Recursos adicionais e personalizações
- Suporte e atualizações
- Licença com validade anual

👉 **Conheça os planos e adquira sua licença:**

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

```bash
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

O projeto possui duas camadas de uso:

### 📂 Código-fonte (comunitário)

Disponível sob a **Apache License 2.0**, conforme definido no arquivo [`LICENSE`](LICENSE).

### 💼 Uso profissional

O uso de funcionalidades avançadas está sujeito a licenciamento, conforme descrito nos arquivos:

- [`TERMS.md`](TERMS.md) — Termos de uso
- [`EULA.md`](EULA.md) — Contrato de licença de usuário final
- [`PRICING.md`](PRICING.md) — Planos disponíveis

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
