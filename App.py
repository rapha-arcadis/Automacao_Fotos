import os
import sys
import threading
import subprocess
import customtkinter as ctk
from tkinter import messagebox

from Scripts.Components.ClientDataForm import ClientDataForm
from Scripts.Components.PathSelector import PathSelector
from Scripts.Components.ProgressBar import ProgressBar


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def abrir_diretorio(caminho_arquivo):
    caminho_arquivo = os.path.abspath(caminho_arquivo)
    pasta = os.path.dirname(caminho_arquivo)
    if sys.platform.startswith("win"):
        subprocess.Popen(["explorer", "/select,", caminho_arquivo])
    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["open", pasta])
    else:
        subprocess.Popen(["xdg-open", pasta])


ctk.set_appearance_mode("light")
ctk.set_default_color_theme(resource_path("theme/arcadis_theme.json"))


class App(ctk.CTk):
    """Main UI orchestrator. Blind to business logic and APIs."""

    def __init__(self, process_service, client_list):
        super().__init__()

        self.geometry("550x480")
        self.title("Renomeador de arquivos")
        self.iconbitmap(resource_path("assets/arcadis_logo.ico"))

        self.process_service = process_service
        self.etl_result = None
        self.etl_error = None

        # Header
        self.title_label = ctk.CTkLabel(
            self,
            text="Renomeação de Arquivos",
            font=("FS Elliot Pro", 28, "bold"),
            text_color="#494646",
        )
        self.title_label.pack(pady=(45, 0))

        # Subtítulo
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Selecione o diretório de entrada, o arquivo Excel e a pasta de saída",
            font=("FS Elliot Pro", 15, "bold"),
            text_color="#7a7a7a",
        )
        self.subtitle_label.pack(pady=(2, 10))

        self.container_central = ctk.CTkFrame(master=self, fg_color="transparent")
        self.container_central.pack(expand=True, fill="both")

        self.conteudo_wrapper = ctk.CTkFrame(
            master=self.container_central, fg_color="transparent"
        )
        self.conteudo_wrapper.pack(expand=True, fill="x", padx=35)

        # --- COMPONENTS INJECTION ---

        self.path_selector = PathSelector(master=self.conteudo_wrapper)
        self.path_selector.pack(fill="x", pady=(0, 20))

        # O botão submit está encapsulado dentro do formulário
        self.client_form = ClientDataForm(
            master=self.conteudo_wrapper,
            client_list=client_list,
            submit_command=self.validate_and_submit,
        )
        self.client_form.pack(fill="x", pady=(0, 20))

        # --- PROGRESS BAR COMPONENT ---
        # Instanciamos o componente e garantimos que ele seja desenhado na tela
        self.progress = ProgressBar(master=self.conteudo_wrapper)
        self.progress.pack(fill="x")

    def validate_and_submit(self):
        paths = self.path_selector.get_paths()
        if not paths["input_path"]:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecione o arquivo Excel de entrada antes de continuar.",
            )
            return
        if not paths["base_path"]:
            messagebox.showwarning(
                "Aviso", "Por favor, selecione o diretório de saída antes de continuar."
            )
            return

        kwargs_etl = {**paths}

        # UI Lock (Trava os formulários e botões)
        self.client_form.lock()
        self.path_selector.lock()

        # Inicia o visual da barra (se o seu componente tiver a função set_processing)
        if hasattr(self.progress, "set_processing"):
            self.progress.set_processing()

        self.etl_result = None
        self.etl_error = None

        # Inicia a Thread passando os dados
        thread = threading.Thread(
            target=self._run_service_in_background, args=(kwargs_etl,), daemon=True
        )
        thread.start()

        # Chama o monitor de término (não anima mais sozinho!)
        self._monitor_thread(thread)

    def _run_service_in_background(self, kwargs):
        try:
            # A MÁGICA DO LABEL DINÂMICO AQUI:
            # Injetamos a função de atualização real no serviço!
            self.etl_result = self.process_service(
                **kwargs, progress_callback=self.atualizar_progresso_real
            )
        except Exception as e:
            self.etl_error = str(e)

    def atualizar_progresso_real(self, valor, texto=None):
        """
        Esta função é chamada lá de dentro do seu processador de dados (main/Pandas).
        Ela envia o valor da barra e o texto atual para a interface gráfica.
        """
        # Atualiza a barra
        self.progress.update_progress(valor)

        # Atualiza a label dinamicamente
        if texto and hasattr(self.progress, "status_label"):
            self.progress.status_label.configure(text=texto)

    def _monitor_thread(self, thread):
        """Apenas vigia se a thread do backend já terminou."""
        if thread.is_alive():
            # Fica perguntando a cada 100ms se terminou
            self.after(100, lambda: self._monitor_thread(thread))
        else:
            # UI Unlock (Destrava botões e entradas)
            self.client_form.unlock()
            self.path_selector.unlock()

            # Checa os resultados
            if self.etl_error:
                if hasattr(self.progress, "set_error"):
                    self.progress.set_error()
                messagebox.showerror(
                    "Erro no Processamento", f"Ocorreu um erro:\n{self.etl_error}"
                )
            else:
                if hasattr(self.progress, "set_success"):
                    self.progress.set_success()
                messagebox.showinfo(
                    "Sucesso", "Arquivo gerado e exportado com sucesso!"
                )
                abrir_diretorio(self.etl_result)
                self.path_selector.reset()

            # Após 2 segundos do fim, reseta a interface inteira de volta ao normal
            if hasattr(self.progress, "reset"):
                self.after(2000, self.progress.reset)
