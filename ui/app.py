"""
Interface gráfica principal do ApT usando CustomTkinter.

Thread safety: todos os callbacks de thread usam self.after(0, fn)
para atualizar widgets apenas na thread da UI.
"""
import os
import threading
import platform
import webbrowser

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image as PILImage

from core.transcriber import transcrever_arquivos, EXTENSOES_SUPORTADAS
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

        # ── Header com logo ──
        frame_header = ctk.CTkFrame(self, fg_color="transparent")
        frame_header.pack(fill="x", padx=16, pady=(14, 8))

        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "app_icon.png")
        if os.path.exists(logo_path):
            pil_img = PILImage.open(logo_path)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(56, 56))
            ctk.CTkLabel(frame_header, image=ctk_img, text="").pack(side="left", padx=(0, 12))

        frame_header_text = ctk.CTkFrame(frame_header, fg_color="transparent")
        frame_header_text.pack(side="left", anchor="w")
        ctk.CTkLabel(
            frame_header_text, text="ApT — Áudio para Texto",
            font=ctk.CTkFont(size=18, weight="bold"), anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            frame_header_text, text="Cadeia de custódia digital — Lei 13.964/2019 (Pacote Anticrime)",
            font=ctk.CTkFont(size=10), text_color="gray", anchor="w"
        ).pack(anchor="w")

        # ── Identificação ──
        frame_id = ctk.CTkFrame(self)
        frame_id.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_id, text="Identificação", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkLabel(frame_id, text="Unidade:").grid(row=1, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_id, textvariable=self._unidade_var, width=380).grid(
            row=1, column=1, padx=8, pady=2
        )
        ctk.CTkLabel(frame_id, text="Responsável:").grid(row=2, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_id, textvariable=self._responsavel_var, width=380).grid(
            row=2, column=1, padx=8, pady=(2, 8)
        )

        # ── Pastas ──
        frame_pastas = ctk.CTkFrame(self)
        frame_pastas.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_pastas, text="Pastas", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkLabel(frame_pastas, text="Entrada:").grid(row=1, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_pastas, textvariable=self._input_path, width=320).grid(
            row=1, column=1, padx=4, pady=2
        )
        ctk.CTkButton(frame_pastas, text="Selecionar", width=90,
                      command=self._select_input).grid(row=1, column=2, padx=8, pady=2)

        ctk.CTkLabel(frame_pastas, text="Saída:").grid(row=2, column=0, sticky="w", padx=8, pady=2)
        ctk.CTkEntry(frame_pastas, textvariable=self._output_path, width=320).grid(
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

        # ── Relatório de Transcrição ──
        frame_laudo = ctk.CTkFrame(self)
        frame_laudo.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_laudo, text="Relatório de Transcrição", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkCheckBox(
            frame_laudo,
            text="Gerar relatório PDF com cadeia de custódia (SHA-256)",
            variable=self._gerar_pdf_var,
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=8, pady=2)
        self._label_status_laudo = ctk.CTkLabel(
            frame_laudo, text="", font=ctk.CTkFont(size=11)
        )
        self._label_status_laudo.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

        # ── Licença ──
        frame_lic = ctk.CTkFrame(self)
        frame_lic.pack(fill="x", **PAD)
        ctk.CTkLabel(frame_lic, text="Licença", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 2)
        )
        ctk.CTkButton(
            frame_lic, text="Carregar arquivo .apt_lic", width=200,
            command=self._carregar_licenca
        ).grid(row=1, column=0, padx=8, pady=2, sticky="w")
        ctk.CTkButton(
            frame_lic, text="Adquirir licença →", width=150,
            fg_color="transparent", border_width=1,
            border_color="#6B21A8", text_color="#A855F7",
            hover_color="#3B1060",
            font=ctk.CTkFont(size=11),
            command=lambda: webbrowser.open("https://www.brunnoml.com.br/produtos/apt/licenca"),
        ).grid(row=1, column=1, padx=8, pady=2, sticky="w")
        self._label_status_lic = ctk.CTkLabel(
            frame_lic, text="", font=ctk.CTkFont(size=11)
        )
        self._label_status_lic.grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

        # ── Progresso ──
        self._progress_bar = ctk.CTkProgressBar(self, width=500)
        self._progress_bar.pack(padx=12, pady=(8, 2))
        self._progress_bar.set(0)

        self._label_progresso = ctk.CTkLabel(self, text="Aguardando...", font=ctk.CTkFont(size=11))
        self._label_progresso.pack(padx=12, pady=(0, 4))

        # ── Botão iniciar ──
        self._btn_iniciar = ctk.CTkButton(
            self, text="Iniciar Transcrição",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#6B21A8", hover_color="#7E22CE",
            height=40, width=240,
            command=self._iniciar_transcricao,
        )
        self._btn_iniciar.pack(pady=(4, 8))

        # ── Histórico ──
        ctk.CTkLabel(self, text="Histórico", font=ctk.CTkFont(size=11), text_color="gray").pack(
            padx=12, anchor="w"
        )
        self._log = ctk.CTkTextbox(self, width=520, height=80, state="disabled",
                                   font=ctk.CTkFont(size=11))
        self._log.pack(padx=12, pady=(2, 14))

    # ──────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────

    def _carregar_icone(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.normpath(os.path.join(base_dir, "..", "images"))
        ico_path = os.path.join(images_dir, "apt.ico")   # ícone janela/taskbar
        png_path = os.path.join(images_dir, "app_icon.png")   # fallback não-Windows

        if platform.system() == "Windows":
            try:
                import ctypes
                import ctypes.wintypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("BrunnoML.ApT.1")
            except Exception:
                pass
            if os.path.exists(ico_path):
                def _set_win_icon():
                    self.iconbitmap(ico_path)
                    try:
                        import ctypes
                        user32 = ctypes.windll.user32
                        hwnd = self.winfo_id()
                        LR_LOADFROMFILE = 0x00000010
                        IMAGE_ICON = 1
                        WM_SETICON = 0x0080
                        ICON_SMALL, ICON_BIG = 0, 1
                        GCLP_HICON, GCLP_HICONSM = -14, -34
                        # Usa tamanhos definidos pelo sistema (respeita DPI do Windows)
                        cx_icon = user32.GetSystemMetrics(11)   # SM_CXICON
                        cy_icon = user32.GetSystemMetrics(12)   # SM_CYICON
                        cx_sm   = user32.GetSystemMetrics(49)   # SM_CXSMICON
                        cy_sm   = user32.GetSystemMetrics(50)   # SM_CYSMICON
                        hicon_large = user32.LoadImageW(
                            None, ico_path, IMAGE_ICON, cx_icon, cy_icon, LR_LOADFROMFILE
                        )
                        hicon_small = user32.LoadImageW(
                            None, ico_path, IMAGE_ICON, cx_sm, cy_sm, LR_LOADFROMFILE
                        )
                        if hicon_large:
                            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_large)
                            # Define também no window class (usado pela barra de tarefas)
                            user32.SetClassLongPtrW(hwnd, GCLP_HICON, hicon_large)
                        if hicon_small:
                            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
                            user32.SetClassLongPtrW(hwnd, GCLP_HICONSM, hicon_small)
                    except Exception:
                        pass
                self.after_idle(_set_win_icon)
        elif os.path.exists(png_path):
            try:
                from PIL import ImageTk
                pil_img = PILImage.open(png_path)
                self._icon_img = ImageTk.PhotoImage(pil_img)
                self.iconphoto(True, self._icon_img)
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
            messagebox.showwarning("Atenção", "Informe a Unidade para gerar o relatório PDF.")
            return
        if gerar_pdf and not responsavel:
            messagebox.showwarning("Atenção", "Informe o Responsável para gerar o relatório PDF.")
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
                "Você já utilizou o relatório gratuito disponível na versão de teste.\n\n"
                "Para relatórios ilimitados, adquira a licença do ApT.\n\n"
                "Carregue o arquivo .apt_lic na seção Licença Premium."
            )
            return

        self._btn_iniciar.configure(state="disabled")
        self._progress_bar.set(0)
        self._label_progresso.configure(text="Iniciando...")
        n_audio = sum(1 for f in os.listdir(input_path) if f.lower().endswith(EXTENSOES_SUPORTADAS))
        self._log_append(f"Iniciando — modelo {model_name.upper()}, {n_audio} arquivo(s) de áudio")

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
            self._label_progresso.configure(text=f"Processando {atual} de {total}: {nome}")
            self._log_append(f"{atual}/{total}  {nome}")
        self.after(0, _update)

    def _cb_concluido(self, msg: str, pdf_path: str | None, hash_pdf: str | None) -> None:
        def _update():
            self._progress_bar.set(1.0)
            self._label_progresso.configure(text="Concluído!")
            self._btn_iniciar.configure(state="normal")
            self._log_append("Concluído com sucesso.")
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
