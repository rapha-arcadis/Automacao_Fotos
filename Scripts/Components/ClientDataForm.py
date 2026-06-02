import customtkinter as ctk


class ClientDataForm(ctk.CTkFrame):
    """Component that holds the form fields and the submit action."""

    # Recebe o submit_command que virá do App.py
    def __init__(self, master, submit_command, **kwargs):
        super().__init__(
            master,
            fg_color=("#FFB786", "#F49A5E"),
            border_color="#E56011",
            border_width=2,
            **kwargs
        )

        # Divide o frame em duas colunas de tamanhos iguais
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Coluna 0: Tipo de conversão (Label e ComboBox) ---
        self.opcoes = ["Imagens", "Videos"]
        self.label_tipo = ctk.CTkLabel(
            self, text="Tipo de conversão", font=("Arial", 12, "bold")
        )
        self.label_tipo.grid(row=0, column=0, sticky="w", padx=(20, 10), pady=(15, 5))

        self.entry_tipo = ctk.CTkComboBox(self, values=self.opcoes, state="readonly")
        self.entry_tipo.grid(row=1, column=0, sticky="ew", padx=(20, 10), pady=(0, 20))

        # Helper to open dropdown on click
        self.entry_tipo._entry.bind("<Button-1>", lambda e: self.entry_tipo._clicked())

        # --- Coluna 1: Botão Submit ---
        self.btn_submit = ctk.CTkButton(
            self,
            text="Submit",
            height=30,  # Ajustado para alinhar melhor com a altura do combo
            command=submit_command,  # Liga o botão à função que veio do App
        )
        # O botão fica na mesma linha (row=1) do ComboBox, mas na coluna do lado (column=1)
        self.btn_submit.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=(0, 20))

    def get_data(self):
        """Returns all text inputs as a dictionary."""
        return {"matrix_name": self.entry_tipo.get()}

    # Centralizamos o travamento do form e do botão no mesmo lugar
    def lock(self):
        self.entry_tipo.configure(state="disabled")
        self.btn_submit.configure(text="Processando...", state="disabled")

    def unlock(self):
        self.entry_tipo.configure(state="readonly")
        self.btn_submit.configure(text="Submit", state="normal")
