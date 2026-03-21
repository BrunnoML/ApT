"""
Interface gráfica principal do ApT usando CustomTkinter.

Thread safety: todos os callbacks de thread usam self.after(0, fn)
para atualizar widgets apenas na thread da UI.
"""
import os
import threading
import platform

import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.transcriber import transcrever_arquivos
from licensing.license_manager import (
    pode_gerar_laudo,
    pode_transcrever,
    registrar_laudo,
    tem_licenca_ativa,
    get_status_licenca,
    ativar_licenca,
    MAX_FREE_LAUDOS,
    MAX_FREE_SEGUNDOS,
    laudos_gerados,
    segundos_restantes_gratis,
)


class AptApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ApT — Áudio para Texto")
        self.resizable(False, False)

        # Ícone
        self._carregar_icone()

        # Variáveis de controle
        self._input_path = ctk.StringVar()
        self._output_path = ctk.StringVar()
        self._model_var = ctk.StringVar(value="large")
        self._unidade_var = ctk.StringVar()
        self._responsavel_var = ctk.StringVar()
        self._gerar_pdf_var = ctk.BooleanVar(value=True)

        self._build_ui()
        self._atualizar_status_licenca()

    # ──────────────────────────────────────────────────────────────
    # Construção da UI
    # ──────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        PAD = {"padx": 12, "pady": 4}

        # Título
        ctk.CTkLabel(
            self, text="ApT — Áudio para Texto",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=12, pady=(14, 2))
        ctk.CTkLabel(
            self, text="Transcrição forense com cadeia de custódia — Lei 13.964/2019",
            font=ctk.CTkFont(size=11), text_color="gray"
        ).pack(padx=12, pady=(0, 10))

        # ── Identificação ──
        frame_id = ctk.CTkFrame(self)
        frame_id.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_id, text="Identificação", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkLabel(frame_id, text="Unidade:").grid(row=1, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_id, textvariable=self._unidade_var, width=340).grid(
            row=1, column=1, padx=8, pady=2
        )
        ctk.CTkLabel(frame_id, text="Responsável:").grid(row=2, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_id, textvariable=self._responsavel_var, width=340).grid(
            row=2, column=1, padx=8, pady=(2, 8)
        )

        # ── Pastas ──
        frame_pastas = ctk.CTkFrame(self)
        frame_pastas.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_pastas, text="Pastas", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkLabel(frame_pastas, text="Entrada:").grid(row=1, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_pastas, textvariable=self._input_path, width=280).grid(
            row=1, column=1, padx=4, pady=2
        )
        ctk.CTkButton(frame_pastas, text="Selecionar", width=90,
                      command=self._select_input).grid(row=1, column=2, padx=8, pady=2)

        ctk.CTkLabel(frame_pastas, text="Saída:").grid(row=2, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_pastas, textvariable=self._output_path, width=280).grid(
            row=2, column=1, padx=4, pady=2
        )
        ctk.CTkButton(frame_pastas, text="Selecionar", width=90,
                      command=self._select_output).grid(row=2, column=2, padx=8, pady=(2, 8))

        # ── Modelo Whisper ──
        frame_modelo = ctk.CTkFrame(self)
        frame_modelo.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_modelo, text="Modelo Whisper", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(6, 2)
        )
        for col, (valor, texto) in enumerate([
            ("base", "base — rápido"),
            ("medium", "medium — equilibrado"),
            ("large", "large — melhor qualidade ⭐"),
        ]):
            ctk.CTkRadioButton(
                frame_modelo, text=texto, variable=self._model_var, value=valor
            ).grid(row=1, column=col, padx=10, pady=(2, 8), sticky="w")

        # ── Laudo Forense ──
        frame_laudo = ctk.CTkFrame(self)
        frame_laudo.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_laudo, text="Laudo Forense", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkCheckBox(
            frame_laudo,
            text="Gerar laudo PDF com cadeia de custódia (SHA-256)",
            variable=self._gerar_pdf_var,
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=8, pady=2)
        self._label_status_laudo = ctk.CTkLabel(
            frame_laudo, text="", font=ctk.CTkFont(size=11)
        )
        self._label_status_laudo.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

        # ── Licença ──
        frame_lic = ctk.CTkFrame(self)
        frame_lic.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_lic, text="Licença Premium", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkButton(
            frame_lic, text="Carregar arquivo .apt_lic", width=200,
            command=self._carregar_licenca
        ).grid(row=1, column=0, padx=8, pady=2, sticky="w")
        self._label_status_lic = ctk.CTkLabel(
            frame_lic, text="", font=ctk.CTkFont(size=11)
        )
        self._label_status_lic.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

        # ── Progresso ──
        self._progress_bar = ctk.CTkProgressBar(self, width=440)
        self._progress_bar.pack(padx=12, pady=(8, 2))
        self._progress_bar.set(0)

        self._label_progresso = ctk.CTkLabel(self, text="Aguardando...", font=ctk.CTkFont(size=11))
        self._label_progresso.pack(padx=12, pady=(0, 4))

        # ── Botão iniciar ──
        self._btn_iniciar = ctk.CTkButton(
            self, text="Iniciar Transcrição",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#6B21A8", hover_color="#7E22CE",
            height=40, width=220,
            command=self._iniciar_transcricao,
        )
        self._btn_iniciar.pack(pady=(4, 8))

        # ── Log ──
        self._log = ctk.CTkTextbox(self, width=480, height=120, state="disabled")
        self._log.pack(padx=12, pady=(0, 14))

    # ──────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────

    def _carregar_icone(self) -> None:
        os_type = platform.system()
        icon_path = os.path.join("images", f"app_icon.{'ico' if os_type == 'Windows' else 'png'}")
        if os.path.exists(icon_path):
            try:
                if os_type == "Windows":
                    self.iconbitmap(icon_path)
                else:
                    import tkinter as tk
                    img = tk.PhotoImage(file=icon_path)
                    self.iconphoto(False, img)
            except Exception:
                pass

    def _log_append(self, texto: str) -> None:
        self._log.configure(state="normal")
        self._log.insert("end", texto + "\n")
        self._log.see("end")
        self._log.configure(state="disabled")

    def _atualizar_status_licenca(self) -> None:
        status = get_status_licenca()
        limite_atingido = (
            not status["valida"]
            and (laudos_gerados() >= MAX_FREE_LAUDOS or segundos_restantes_gratis() <= 0)
        )
        cor = "#22C55E" if status["valida"] else ("#EF4444" if limite_atingido else "#3B82F6")
        self._label_status_laudo.configure(text=status["mensagem"], text_color=cor)
        self._label_status_lic.configure(
            text="Licença ativa" if status["valida"] else "Sem licença premium",
            text_color="#22C55E" if status["valida"] else "gray"
        )

    def _select_input(self) -> None:
        pasta = filedialog.askdirectory()
        if pasta:
            self._input_path.set(os.path.normpath(pasta))

    def _select_output(self) -> None:
        pasta = filedialog.askdirectory()
        if pasta:
            self._output_path.set(os.path.normpath(pasta))

    def _carregar_licenca(self) -> None:
        caminho = filedialog.askopenfilename(
            title="Selecionar licença .apt_lic",
            filetypes=[("Arquivo de licença ApT", "*.apt_lic"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
        sucesso, msg = ativar_licenca(caminho)
        if sucesso:
            messagebox.showinfo("Licença ativada", msg)
        else:
            messagebox.showerror("Licença inválida", msg)
        self._atualizar_status_licenca()

    # ──────────────────────────────────────────────────────────────
    # Transcrição
    # ──────────────────────────────────────────────────────────────

    def _iniciar_transcricao(self) -> None:
        input_path = self._input_path.get()
        output_path = self._output_path.get()
        unidade = self._unidade_var.get().strip()
        responsavel = self._responsavel_var.get().strip()
        gerar_pdf = self._gerar_pdf_var.get()
        model_name = self._model_var.get()

        if not input_path:
            messagebox.showwarning("Atenção", "Selecione a pasta de entrada.")
            return
        if not output_path:
            messagebox.showwarning("Atenção", "Selecione a pasta de saída.")
            return
        if gerar_pdf and not unidade:
            messagebox.showwarning("Atenção", "Informe a Unidade para gerar o laudo PDF.")
            return
        if gerar_pdf and not responsavel:
            messagebox.showwarning("Atenção", "Informe o Responsável para gerar o laudo PDF.")
            return
        if not tem_licenca_ativa() and not pode_transcrever():
            messagebox.showinfo(
                "Versão Gratuita — Limite Atingido",
                f"Você já processou {MAX_FREE_SEGUNDOS // 60} minutos de áudio na versão gratuita.\n\n"
                "Para processamento ilimitado, adquira a licença do ApT.\n\n"
                "Carregue o arquivo .apt_lic na seção Licença Premium."
            )
            return

        if gerar_pdf and not pode_gerar_laudo():
            messagebox.showinfo(
                "Versão Gratuita — Limite Atingido",
                "Você já utilizou o laudo gratuito disponível na versão de teste.\n\n"
                "Para laudos ilimitados, adquira a licença do ApT.\n\n"
                "Carregue o arquivo .apt_lic na seção Licença Premium."
            )
            return

        self._btn_iniciar.configure(state="disabled")
        self._progress_bar.set(0)
        self._label_progresso.configure(text="Iniciando...")
        self._log_append(f"[Iniciando] modelo={model_name}, PDF={gerar_pdf}")

        threading.Thread(
            target=transcrever_arquivos,
            args=(
                input_path, output_path, model_name, gerar_pdf,
                unidade, responsavel,
                self._cb_progresso,
                self._cb_concluido,
                self._cb_erro,
            ),
            daemon=True,
        ).start()

    # ──────────────────────────────────────────────────────────────
    # Callbacks thread-safe (sempre via self.after)
    # ──────────────────────────────────────────────────────────────

    def _cb_progresso(self, atual: int, total: int, nome: str) -> None:
        def _update():
            self._progress_bar.set(atual / total)
            self._label_progresso.configure(text=f"Processando {atual}/{total}: {nome}")
            self._log_append(f"[{atual}/{total}] {nome}")
        self.after(0, _update)

    def _cb_concluido(self, msg: str, pdf_path: str | None, hash_pdf: str | None) -> None:
        def _update():
            self._progress_bar.set(1.0)
            self._label_progresso.configure(text="Concluído!")
            self._btn_iniciar.configure(state="normal")
            self._log_append("[Concluído]")
            if pdf_path:
                registrar_laudo()
                self._atualizar_status_licenca()
            messagebox.showinfo("Concluído!", msg)
        self.after(0, _update)

    def _cb_erro(self, msg: str) -> None:
        def _update():
            self._btn_iniciar.configure(state="normal")
            self._label_progresso.configure(text="Erro.")
            self._log_append(f"[Erro] {msg}")
            messagebox.showerror("Erro", msg)
        self.after(0, _update)
