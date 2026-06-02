import os
import sys
import threading
import subprocess
import customtkinter as ctk
from tkinter import messagebox

from Scripts.Components.ClientDataForm import ClientDataForm
from Scripts.Components.PathSelector import PathSelector

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

        self.geometry("480x430")
        self.title("Resultados EQuis")
        self.iconbitmap(resource_path("assets/arcadis_logo.ico"))

        self.process_service = process_service
        self.etl_result = None
        self.etl_error = None

        self.container_central = ctk.CTkFrame(master=self, fg_color="transparent")
        self.container_central.pack(expand=True, fill="both")

        self.conteudo_wrapper = ctk.CTkFrame(master=self.container_central, fg_color="transparent")
        self.conteudo_wrapper.pack(expand=True, fill="x", padx=35)

        # --- COMPONENTS INJECTION ---
        
        # self.client_form = ClientDataForm(master=self.conteudo_wrapper, client_list=client_list)
        # self.client_form.pack(fill="x", pady=(0, 20))

        self.path_selector = PathSelector(master=self.conteudo_wrapper)
        self.path_selector.pack(fill="x", pady=(0, 20))

        # --- PROGRESS & SUBMIT ---
        
        self.progressbar = ctk.CTkProgressBar(self.conteudo_wrapper)
        self.progressbar.pack(fill="x", pady=(20, 20))
        self.progressbar.set(0)

        self.btn_submit = ctk.CTkButton(
            self.conteudo_wrapper, text="Submit", height=40, command=self.validate_and_submit
        )
        self.btn_submit.pack(fill="x", pady=(10, 0))

    def validate_and_submit(self):
        paths = self.path_selector.get_paths()
        if not paths["input_path"]:
            messagebox.showwarning("Aviso", "Por favor, selecione o arquivo Excel de entrada antes de continuar.")
            return
        if not paths["base_path"]:
            messagebox.showwarning("Aviso", "Por favor, selecione o diretório de saída antes de continuar.")
            return

        form_data = self.client_form.get_data()
        if not form_data["client_name"] or not form_data["matrix_name"]:
            messagebox.showwarning("Aviso", "Os campos 'Nome do cliente' e 'Matriz' são obrigatórios.")
            return

        # Merges the dictionaries dynamically
        kwargs_etl = {**paths, **form_data}

        # UI Lock
        self.progressbar.set(0)
        self.btn_submit.configure(text="Processando", state="disabled")
        self.client_form.lock()
        self.path_selector.lock()

        self.etl_result = None
        self.etl_error = None

        thread = threading.Thread(target=self._run_service_in_background, args=(kwargs_etl,), daemon=True)
        thread.start()
        self.animate_progress(thread)

    def _run_service_in_background(self, kwargs):
        try:
            self.etl_result = self.process_service(**kwargs)
        except Exception as e:
            self.etl_error = str(e)

    def animate_progress(self, thread):
        if thread.is_alive():
            valor = min(self.progressbar.get() + 0.02, 0.95)
            self.progressbar.set(valor)
            self.after(100, lambda: self.animate_progress(thread))
        else:
            self.progressbar.set(1)
            self.btn_submit.configure(text="Submit", state="normal")
            
            # UI Unlock
            self.client_form.unlock()
            self.path_selector.unlock()

            if self.etl_error:
                messagebox.showerror("Erro no Processamento", f"Ocorreu um erro:\n{self.etl_error}")
                self.progressbar.set(0)
            else:
                messagebox.showinfo("Sucesso", "Arquivo gerado e exportado com sucesso!")
                abrir_diretorio(self.etl_result)
                self.after(1000, lambda: self.progressbar.set(0))
                self.path_selector.reset()