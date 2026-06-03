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
    """
    Main UI orchestrator. Blind to business logic and APIs.
    """

    def __init__(self, process_service):
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

        # Frame dos botões
        self.path_selector = PathSelector(master=self.conteudo_wrapper)
        self.path_selector.pack(fill="x", pady=(0, 20))

        # Frame inferior com combobox e botão
        self.client_form = ClientDataForm(
            master=self.conteudo_wrapper,
            submit_command=self.validate_and_submit,
        )
        self.client_form.pack(fill="x", pady=(0, 20))

        # Progressbar
        self.progress = ProgressBar(master=self.conteudo_wrapper)
        self.progress.pack(fill="x")

    def validate_and_submit(self):
        """
        Valida os caminhos e dados do formulário antes de iniciar o processamento.
        Se todas as validações passarem, trava a interface, inicia a barra de progresso
        e dispara o serviço ETL em uma thread separada para não travar a UI.
        """
        # Obtém os caminhos selecionados pelo usuário (entrada, Excel e saída)
        paths = self.path_selector.get_paths()

        # Pega a escolha do formulário (Imagens ou Vídeos)
        form_data = self.client_form.get_data()

        # Exibe aviso e interrompe se algum caminho estiver vazio
        if not paths["input_path"]:
            messagebox.showwarning(
                "Aviso", "Por favor, selecione o diretório de entrada."
            )
            return
        if not paths["excel_path"]:
            messagebox.showwarning(
                "Aviso",
                "Por favor, selecione o arquivo Excel de entrada antes de continuar.",
            )
            return
        if not paths["base_path"]:
            messagebox.showwarning(
                "Aviso", "Por favor, selecione o diretório de saída."
            )
            return

        # Junta os caminhos com o tipo de conversão escolhido em um único dicionário
        kwargs_etl = {**paths, "tipo_conversao": form_data["matrix_name"]}

        # UI Lock — Trava os formulários e botões para evitar alterações durante o processamento
        self.client_form.lock()
        self.path_selector.lock()

        # Inicia o visual da barra de progresso (modo "processando")
        if hasattr(self.progress, "set_processing"):
            self.progress.set_processing()

        # Limpa resultados e erros de execuções anteriores
        self.etl_result = None
        self.etl_error = None

        # Inicia uma Thread daemon passando os dados para o serviço ETL rodar em segundo plano
        thread = threading.Thread(
            target=self._run_service_in_background, args=(kwargs_etl,), daemon=True
        )
        thread.start()

        # Chama o monitor que fica verificando periodicamente se a thread já terminou
        self._monitor_thread(thread)

    def _run_service_in_background(self, kwargs):
        """
        Executa o serviço de processamento (ETL) em segundo plano.
        Armazena o resultado em self.etl_result ou, em caso de falha,
        captura a exceção e salva a mensagem de erro em self.etl_error.
        """
        try:
            # Chama o serviço principal, passando os caminhos, tipo de conversão
            # e o callback para atualização em tempo real da barra de progresso
            self.etl_result = self.process_service(
                **kwargs, progress_callback=self.atualizar_progresso_real
            )
        except Exception as e:
            # Captura qualquer erro para exibição posterior na interface
            self.etl_error = str(e)

    def atualizar_progresso_real(self, valor, texto=None):
        """
        Callback chamado pela thread secundária.
        Usa self.after() para agendar a atualização na MAIN THREAD,
        garantindo que nenhum widget seja tocado fora dela.
        """
        self.after(0, self._apply_progress_update, valor, texto)

    def _apply_progress_update(self, valor, texto):
        """
        Executado na main thread — seguro para manipular widgets.
        """
        self.progress.update_progress(valor)
        if texto and hasattr(self.progress, "status_label"):
            self.progress.status_label.configure(text=texto)

    def _monitor_thread(self, thread):
        """
        Monitora periodicamente (a cada 100ms) se a thread do backend já terminou.
        Quando a thread finaliza, destrava a interface e trata o resultado
        (exibindo erro, sucesso ou aviso de arquivos sem correspondência).
        """
        # Se a thread ainda está rodando, reagenda a verificação após 100ms
        if thread.is_alive():
            self.after(100, lambda: self._monitor_thread(thread))
        else:
            # UI Unlock — Destrava botões e entradas para permitir nova interação
            self.client_form.unlock()
            self.path_selector.unlock()

            # Checa os resultados da execução do ETL
            if self.etl_error:
                # Atualiza a barra para estado de erro, se suportado
                if hasattr(self.progress, "set_error"):
                    self.progress.set_error()
                # Exibe o erro ao usuário
                messagebox.showerror(
                    "Erro no Processamento", f"Ocorreu um erro:\n{self.etl_error}"
                )
            else:
                # Atualiza a barra para estado de sucesso, se suportado
                if hasattr(self.progress, "set_success"):
                    self.progress.set_success()

                # Extrai dados do resultado retornado pelo serviço
                resultado = self.etl_result
                diretorio_saida = resultado["base_path"]
                houve_arquivos_perdidos = resultado["tem_nao_correspondidos"]

                # Verifica se houve arquivos sem correspondência no Excel
                if houve_arquivos_perdidos:
                    messagebox.showwarning(
                        "Aviso",
                        "Processamento concluído, mas alguns arquivos não tinham correspondência no Excel!\n\n"
                        "O arquivo 'arquivos_sem_correspondencia.txt' foi gerado.",
                    )
                    abrir_diretorio(resultado["txt_path"])
                else:
                    messagebox.showinfo(
                        "Sucesso",
                        "Todos os arquivos foram mapeados, renomeados e exportados com sucesso!",
                    )

                # Abre o diretório onde os arquivos (e o TXT, se existir) foram salvos
                abrir_diretorio(diretorio_saida)

                # Reseta os campos de caminho para uma nova execução
                self.path_selector.reset()

            # Após 2 segundos do fim, reseta a barra de progresso de volta ao estado inicial
            if hasattr(self.progress, "reset"):
                self.after(2000, self.progress.reset)
