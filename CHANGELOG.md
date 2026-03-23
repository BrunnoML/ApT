# Changelog

Todas as mudanças relevantes do ApT são documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.1.0] - 2026-03-23

### Adicionado
- Suporte a novos formatos de áudio:

  | Extensão | Origem principal |
  |----------|-----------------|
  | `.opus`  | WhatsApp (mensagens de voz atuais), Signal, Viber |
  | `.amr`   | Android (versões antigas do WhatsApp, gravadores nativos) |
  | `.awb`   | AMR Wideband — variante de `.amr` |
  | `.3gp`   | Gravador nativo Android, extrações UFED/Cellebrite |
  | `.m4b`   | iOS Voice Memos (formato com marcadores) |
  | `.oga`   | Variante de `.ogg` usada por alguns apps |

- Lista de formatos aceitos exibida na interface, abaixo do campo de pasta de entrada

### Corrigido
- Arquivos de áudio corrompidos ou ilegíveis agora registram mensagem clara no relatório (`[ARQUIVO ILEGÍVEL: ...]`) em vez do despejo completo de log do FFmpeg
- Adicionado timeout adaptativo na transcrição:
  - **30 segundos** para arquivos que o mutagen não consegue ler (forte sinal de corrupção)
  - **120 segundos** para arquivos com metadados válidos
  — evita que o app trave indefinidamente em arquivos que causam hang no FFmpeg

---

## [1.0.0] - 2026-03-22

### Lançamento inicial

- Interface gráfica com tema escuro (CustomTkinter)
- Transcrição de áudio local com modelos Whisper: `base`, `medium`, `large`
- Processamento em lote — selecione a pasta e processe todos os áudios de uma vez
- Exportação de transcrições em `.txt` com hash SHA-256 de cada arquivo
- Geração de laudo técnico em PDF com cadeia de custódia (Lei 13.964/2019)
- FFmpeg embutido — sem instalação adicional
- Sistema de licenciamento: gratuita (30 min / 1 laudo) · mensal · anual
