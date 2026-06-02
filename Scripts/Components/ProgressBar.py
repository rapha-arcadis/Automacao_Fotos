import customtkinter


class ProgressBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        # Transparent frame to inherit the application's background color
        super().__init__(master, fg_color="transparent", **kwargs)

        # Status label visual settings
        self.status_label = customtkinter.CTkLabel(
            self,
            text="Aguardando arquivos...",
            font=("FS Elliot Pro", 12, "bold"),
            text_color="gray60",
        )
        self.status_label.pack(anchor="w")

        # Progress bar visual settings
        self.progressbar = customtkinter.CTkProgressBar(
            self, height=10, progress_color="#E4610F"
        )
        self.progressbar.pack(fill="x")
        self.progressbar.set(0)

    # State methods
    def set_processing(self):
        self.status_label.configure(
            text="Lendo e formatando dados...",
            text_color="#E4610F",
            font=("FS Elliot Pro", 12, "bold"),
        )
        self.progressbar.set(0)

    def update_progress(self, value):
        self.progressbar.set(value)
        return self.progressbar.get()

    def set_success(self):
        self.progressbar.set(1)
        self.status_label.configure(
            text="Concluído com sucesso!",
            text_color="green",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def set_file_open(self):
        self.progressbar.set(0)
        self.status_label.configure(
            text="Operação cancelada (Arquivo em uso).",
            text_color="red",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def set_error(self):
        self.progressbar.set(0)
        self.status_label.configure(
            text="Erro no processamento.",
            text_color="red",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def reset(self):
        self.progressbar.set(0)
        self.status_label.configure(
            text="Aguardando arquivo...",
            text_color="gray60",
            font=("FS Elliot Pro", 12, "bold"),
        )
