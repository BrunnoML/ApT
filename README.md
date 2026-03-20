<h1 align="center"> ApT - Áudio para Texto </h1>

<p align="center">
Projeto para transcrever arquivos de áudio para texto.
</p>

<p align="center">
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-funcionalidades">Funcionalidades</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
   <a href="#-configuração">Configuração</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-licença">Licença</a>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=MIT&color=49AA26&labelColor=000000">
</p>

<br>

<p align="center">
  <img alt="ApT" src="/images/preview.png" width="600px">
</p>

## 🚀 Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- Python
- Openai-whisper
- Torch
- Tkinter
- Venv
- Conda
- VSCode
- Git e Github

## 💻 Projeto

Essa aplicação usa a biblioteca Whisper para transcrever arquivos de áudio para texto. Surgiu de uma demanda do trabalho para transcrever uma quantidade grande de arquivos de áudio e facilitar a localização de arquivos relevantes por pesquisa no texto por palavras chaves, de acordo com cada necessidade específica.
Também foi idealizada para usar como projeto de extensão para ser apresentado na faculdade Estádio, no curso Sistemas de Informação.
Pensei em usar ambiente gráfico para facilitar a usabilidade do usuário sem conhecimento em tecnologia.


## 🎯 Funcionalidades

- Abrir um ambiente gráfico usando a biblioteca tkinter;
- Selecionar uma pasta contendo os arquivos de áudio para transcrição;
- Escolher uma pasta para armazenar o arquivo da transcrição no formato `.txt`;
- Selecionar o modelo Whisper (`base`, `medium` ou `large`) para transcrição.

## 🔈 Configuração

#### 1. Baixar o ffmpeg (binários pré-compilados para Windows):

> ⚠️ **Atenção:** Não baixe o código-fonte do site oficial (ffmpeg.org). Baixe os binários prontos para uso no link abaixo.

🔗 https://www.gyan.dev/ffmpeg/builds/

Na seção **"release builds"**, baixe o arquivo: **`ffmpeg-release-essentials.zip`**

#### 2. Extrair e Instalar:

a. Extraia o arquivo ZIP baixado.

b. Dentro do ZIP haverá uma pasta como `ffmpeg-x.x.x-essentials_build\` — entre nela.

c. Copie as pastas `bin\`, `doc\` e `presets\` para `C:\ffmpeg`.

   - 📂 Resultado esperado: `C:\ffmpeg\bin\` deve conter os arquivos `ffmpeg.exe`, `ffplay.exe` e `ffprobe.exe`.

#### 3. Configurar a Variável de Ambiente:

#### Para que o Windows reconheça o FFmpeg no terminal, siga estes passos:

a. Pressione `Win + R`, digite `sysdm.cpl` e pressione Enter.

b. Vá até a aba **Avançado** → clique em **Variáveis de Ambiente**.

c. Na seção **Variáveis do Sistema**, encontre `Path` e clique em **Editar**.

d. Clique em **Novo** e cole `C:\ffmpeg\bin`.

e. Clique em **OK** para salvar.

#### 4. Testar a Instalação:

Abra o Prompt de Comando (cmd) ou PowerShell e digite:
```
ffmpeg -version
```
Se estiver instalado corretamente, você verá informações sobre a versão do FFmpeg, como:
```
ffmpeg version 8.x-essentials_build-www.gyan.dev ...
```



## 🛠️ Instalação

Para usar a aplicação localmente, siga os passos abaixo:

1. Clone o repositório:
```
git clone https://github.com/BrunnoML/ApT.git
```

2. Acessar a pasta criada do projeto:
```
cd apt
```

3. Crie o ambiente virtual:

O projeto foi desenvolvido usando a versão 3.12 do Python.
Para usar o ambiente nesta versão, pode criar o ambiente virtual usando o `venv` ou `conda`:

3.1 O venv é padrão do Python, mas não consegue criar um ambiente virtual com uma versão do Python diferente da instalada no seu sistema operacional, portanto, se optar por usar venv, é recomendável instalar previamente o Python na versão 3.12.

- Usando o venv para criar o ambiente virtual (comando utilizado tanto para Windows quanto para macOS:
```
python -m venv .venv
```

OBS: Pode substituir `.venv` pelo nome do ambiente virtual que desejar.

- Ative o ambiente virtual:
  
- No Windows:
```
.venv\Scripts\activate
```

- No macOS/Linux:
```
source .venv/bin/activate
```

- Desative o ambiente virtual:
```
deactivate
```

Após ativar o ambiente virtual, seu prompt deve mudar para algo como (.venv).

3.2 Utilizando o conda para criar o ambiente virtual, Baixe e instale a versão mais recente do [Miniconda] (https://docs.conda.io/en/latest/miniconda.html)

- Criar o ambiente virtual conda com o Python na versão 3.12:
```
conda create -n .venv python=3.12
```

- Ativar o ambiente virtual conda:
  
Obs: se for a primeira vez que for utilizar o conda, primeiro rode: `conda init`
```
conda activate .venv
```

- Desativar o ambiente virtual conda:
```
conda deactivate
```

4. Atualize o pip e instale o setuptools e wheel:

```
pip install --upgrade pip
pip install setuptools==69.5.1 wheel
```

> ⚠️ **Por que usar a versão específica `69.5.1` do setuptools?**
> O pacote `openai-whisper` precisa ser compilado durante a instalação e depende do módulo `pkg_resources`, que faz parte do `setuptools`. Versões mais recentes do `setuptools` (a partir da 71.x) removeram esse módulo como importável direto, causando o erro `ModuleNotFoundError: No module named 'pkg_resources'`.
> A versão `69.5.1` é a mais recente que ainda inclui o `pkg_resources` de forma compatível.
> O pip pode ser atualizado normalmente para a versão mais recente (26.x), pois ele não tem essa limitação.

5. Instale as dependências com o arquivo requirements.txt:
```
pip install --no-build-isolation -r requirements.txt
```

> ℹ️ A flag `--no-build-isolation` faz o pip usar o ambiente virtual atual para compilar os pacotes, em vez de criar um ambiente temporário isolado. Isso garante que o `setuptools` instalado no passo anterior esteja disponível durante a compilação do `openai-whisper`.

6. Execute o programa:
```
python apt.py
```


## 🪪 Licença

Esse projeto está sob a licença MIT.

---

Feito com :coffee: por [BrunnoML](https://www.brunnoml.com.br)
