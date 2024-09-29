<h1 align="center"> ApT - Áudio para Texto </h1>

<p align="center">
Projeto para transcrever arquivos de áudio para texto.
</p>

<p align="center">
  <a href="#-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-funcionalidades">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-instalação">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-licença">Licença</a>
</p>

<p align="center">
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=MIT&color=49AA26&labelColor=000000">
</p>

<br>

<p align="center">
  <img alt="ApT" src="/images/preview.png" width="100%">
</p>

## 🚀 Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- Python
- Openai-whisper
- Torch
- Tkinter
- Venv
- VSCode
- Git e Github

## 💻 Projeto

Essa aplicação usa a biblioteca Whisper para transcrever arquivos de áudio para texto. Surgiu de uma demanda do trabalho para transcrever uma quantidade grande de arquivos de áudio e facilitar a localização de arquivos relevantes por pesquisa no texto por palavras chaves, de acordo com cada necessidade específica.
Também foi idealizada para usar como projeto de extensão para ser apresentado na faculdade Estádio, no curso Sistemas de Informação.
Pensei em usar ambiente gráfico para facilitar a usabilidade do usuário sem conhecimento em tecnologia.

- [Acesse o projeto finalizado, online](https://brunnoml.github.io/ApT/)

## 🎯 Funcionalidades

- Abrir um ambiente gráfico usando a biblioteca tkinter;
- Selecionar uma pasta contendo os arquivos de áudio para transcrição;
- Escolher uma pasta para armazenar o arquivo da transcrição no formato `.txt`;
- Selecionar o modelo Whisper (`base`, `medium` ou `large`) para transcrição.

## 🛠️ Instalação

Para usar a aplicação localmente, siga os passos abaixo:

1. Clone o repositório:
```
git clone https://github.com/BrunnoML/ApT.git
```
2. Instale as dependências com o arquivo requirements.txt:
```
pip install -r requirements.txt
```
3. Execute o programa:
```
python apt.py
```

## 🪪 Licença

Esse projeto está sob a licença MIT.

---

Feito com :coffee: por [BrunnoML](htts://www.brunnoml.com.br)