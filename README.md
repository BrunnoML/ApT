<h1 align="center"> ApT — Áudio para Texto </h1>

<p align="center">
Ferramenta de transcrição forense de áudio para texto, com geração automática de laudo PDF e cadeia de custódia conforme a Lei 13.964/2019 (Pacote Anticrime).
</p>

<p align="center">
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-funcionalidades">Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-planos">Planos</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-configuração">Configuração</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-licença">Licença</a>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=Apache-2.0&color=49AA26&labelColor=000000">
</p>

<br>

<p align="center">
  <img alt="ApT" src="/images/preview.png" width="400px">
</p>

## Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- Python 3.12
- OpenAI Whisper (transcrição de áudio local)
- CustomTkinter (interface moderna)
- ReportLab (geração de PDF forense)
- Mutagen (leitura de metadados de áudio)
- Cryptography — Ed25519 (verificação de licença)
- PyInstaller (empacotamento em executável)
- FFmpeg (conversão de formatos de áudio)

## Projeto

O **ApT** é uma ferramenta para transcrição em massa de arquivos de áudio com foco em **uso forense e jurídico**. Surgiu da necessidade de transcrever grandes volumes de arquivos de áudio e facilitar a localização de conteúdo por palavras-chave, preservando a integridade da prova digital.

O projeto foi idealizado para atender delegacias, batalhões, escritórios de advocacia, promotorias e peritos que necessitam de laudos prontos para juntada ao processo judicial, com cadeia de custódia documentada conforme a **Lei 13.964/2019 (Pacote Anticrime)**.

### Arquitetura modular

```
apt/
├── main.py               ← ponto de entrada
├── core/
│   ├── audio_utils.py    ← hash SHA-256, duração
│   ├── pdf_report.py     ← geração do laudo forense
│   └── transcriber.py   ← transcrição com threading
├── licensing/
│   ├── license_manager.py   ← controle de uso e licença
│   └── license_validator.py ← verificação Ed25519 (chave pública)
├── ui/
│   └── app.py            ← interface CustomTkinter
└── utils/
    └── ffmpeg_setup.py   ← configuração do ffmpeg
```

## Funcionalidades

- Interface gráfica moderna com tema escuro (CustomTkinter)
- Transcrição de áudio 100% local com Whisper (base, medium ou large)
- Suporte a `.m4a`, `.mp3`, `.wav`, `.ogg`, `.mp4`, `.wma`, `.flac`, `.aac`
- Cálculo de hash **SHA-256** de cada arquivo **antes** de qualquer processamento
- Geração de **laudo PDF forense** estruturado com:
  - Cabeçalho: unidade, responsável, data/hora, hostname, modelo Whisper
  - Por arquivo: nome, hash SHA-256, duração e transcrição completa
  - Declaração de conformidade com a Lei 13.964/2019
  - Hash SHA-256 do próprio PDF gerado
- Barra de progresso em tempo real sem travar a interface (threading)
- Log de operações em tempo real
- Sistema de licença por arquivo `.apt_lic` com assinatura criptográfica Ed25519

## Planos

O ApT adota modelo **freemium**. A versão gratuita está disponível para qualquer usuário. Para uso profissional e ilimitado, consulte os planos disponíveis em:

**[https://www.brunnoml.com.br/apt](https://www.brunnoml.com.br/apt)**

Veja também o arquivo [PRICING.md](PRICING.md) para descrição detalhada dos planos.

## Configuração

### 1. Baixar o FFmpeg (binários pré-compilados para Windows)

> **Atenção:** Não baixe o código-fonte do site oficial (ffmpeg.org). Baixe os binários prontos no link abaixo.

**[https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)**

Na seção **"release builds"**, baixe: **`ffmpeg-release-essentials.zip`**

### 2. Extrair e instalar

a. Extraia o arquivo ZIP.

b. Dentro do ZIP haverá uma pasta como `ffmpeg-x.x.x-essentials_build\` — entre nela.

c. Copie as pastas `bin\`, `doc\` e `presets\` para `C:\ffmpeg`.

   - Resultado esperado: `C:\ffmpeg\bin\` deve conter `ffmpeg.exe`, `ffplay.exe` e `ffprobe.exe`.

### 3. Configurar a variável de ambiente

a. Pressione `Win + R`, digite `sysdm.cpl` e pressione Enter.

b. Vá até a aba **Avançado** → clique em **Variáveis de Ambiente**.

c. Na seção **Variáveis do Sistema**, encontre `Path` e clique em **Editar**.

d. Clique em **Novo** e cole `C:\ffmpeg\bin`.

e. Clique em **OK** para salvar.

### 4. Testar a instalação

```
ffmpeg -version
```

Saída esperada:
```
ffmpeg version 8.x-essentials_build-www.gyan.dev ...
```

## Instalação

### 1. Clone o repositório

```
git clone https://github.com/BrunnoML/ApT.git
cd apt
```

### 2. Crie o ambiente virtual

O projeto foi desenvolvido com Python 3.12.

**Usando venv:**

```
python -m venv .venv
```

Ative o ambiente virtual:

- Windows:
```
.venv\Scripts\activate
```

- macOS/Linux:
```
source .venv/bin/activate
```

**Usando conda:**

```
conda create -n apt python=3.12
conda activate apt
```

### 3. Atualize o pip e instale o setuptools

```
pip install --upgrade pip
pip install setuptools==69.5.1 wheel
```

> **Por que `setuptools==69.5.1`?**
> O pacote `openai-whisper` precisa ser compilado e depende do módulo `pkg_resources`, parte do `setuptools`. Versões a partir da 71.x removeram esse módulo, causando `ModuleNotFoundError: No module named 'pkg_resources'`. A versão 69.5.1 é a mais recente compatível.

### 4. Instale as dependências

```
pip install --no-build-isolation -r requirements.txt
```

> A flag `--no-build-isolation` garante que o `setuptools` instalado no passo anterior esteja disponível durante a compilação do `openai-whisper`.

### 5. Execute o programa

```
python main.py
```

Na primeira execução com o modelo `large`, o Whisper irá baixar o modelo (~2,88 GB). Esse download ocorre uma única vez e o modelo fica armazenado localmente.

## Memo Licença

Este projeto é distribuído sob a **Apache License 2.0**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

A versão licenciada (premium) está sujeita ao [EULA](EULA.md).

---

Feito com :coffee: por [BrunnoML](https://www.brunnoml.com.br)
