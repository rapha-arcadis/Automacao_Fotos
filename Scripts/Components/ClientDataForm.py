import customtkinter as ctk

from Scripts.Components.CTkScrollableDropdown import CTkScrollableDropdown

class ClientDataForm(ctk.CTkFrame):
    """Component that holds the form fields for client and project data."""
    
    def __init__(self, master, client_list, **kwargs):
        super().__init__(
            master, 
            fg_color=("#FFB786", "#F49A5E"), 
            border_color="#E56011", 
            border_width=2, 
            **kwargs
        )
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        self.label_titulo = ctk.CTkLabel(self, text="Dados cliente", font=("Arial", 20, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Client Name
        self.label_nome_cliente = ctk.CTkLabel(self, text="Nome do cliente:", font=("Arial", 12, "bold"))
        self.label_nome_cliente.grid(row=1, column=0, sticky="w", padx=(20, 10))
        self.entry_nome_cliente = ctk.CTkEntry(self)
        self.entry_nome_cliente.grid(row=2, column=0, sticky="ew", padx=(20, 10), pady=(0, 15))

        # Requester
        self.label_solicitante = ctk.CTkLabel(self, text="Solicitante:", font=("Arial", 12, "bold"))
        self.label_solicitante.grid(row=1, column=1, sticky="w", padx=(10, 20))
        self.entry_solicitante = ctk.CTkEntry(self)
        self.entry_solicitante.grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=(0, 15))

        # CC
        self.label_cc = ctk.CTkLabel(self, text="CC:", font=("Arial", 12, "bold"))
        self.label_cc.grid(row=3, column=0, sticky="w", padx=(20, 10))
        self.entry_cc = ctk.CTkEntry(self)
        self.entry_cc.grid(row=4, column=0, sticky="ew", padx=(20, 10), pady=(0, 20))

        # Matrix
        self.opcoes = ["Água subterrânea", "Água superficial", "Efluente", "Resíduo", "Sedimento", "Solo", "Vapor"]
        self.label_matriz = ctk.CTkLabel(self, text="Matriz:", font=("Arial", 12, "bold"))
        self.label_matriz.grid(row=3, column=1, sticky="w", padx=(10, 20))
        self.entry_matriz = ctk.CTkComboBox(self, values=self.opcoes, state="readonly")
        self.entry_matriz.grid(row=4, column=1, sticky="ew", padx=(10, 20), pady=(0, 20))
        
        # Helper to open dropdown on click
        self.entry_matriz._entry.bind("<Button-1>", lambda e: self.entry_matriz._clicked())

        # Dropdown configuration using injected list
        def selecionar_cliente(escolha):
            self.entry_nome_cliente.delete(0, "end")
            self.entry_nome_cliente.insert(0, escolha)

        CTkScrollableDropdown(
            self.entry_nome_cliente, 
            values=client_list,
            command=selecionar_cliente,
            autocomplete=True,
            justify="left",
            hover_color="#c8c8c8",
            width=300
        )

    def get_data(self):
        """Returns all text inputs as a dictionary."""
        return {
            "client_name": self.entry_nome_cliente.get(),
            "comp_name": self.entry_solicitante.get(),
            "cc_name": self.entry_cc.get(),
            "matrix_name": self.entry_matriz.get()
        }

    def lock(self):
        self.entry_nome_cliente.configure(state="disabled")
        self.entry_solicitante.configure(state="disabled")
        self.entry_cc.configure(state="disabled")
        self.entry_matriz.configure(state="disabled")

    def unlock(self):
        self.entry_nome_cliente.configure(state="normal")
        self.entry_solicitante.configure(state="normal")
        self.entry_cc.configure(state="normal")
        self.entry_matriz.configure(state="readonly")