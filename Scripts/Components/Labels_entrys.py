import customtkinter

        # Titulo
        self.label_titulo = CTkLabel(master=self.frame_cima, text="Dados cliente", font=("Arial", 20, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Nome do cliente
        self.label_nome_cliente = CTkLabel(master=self.frame_cima, text="Nome do cliente:", font=("Arial", 12, "bold"))
        self.label_nome_cliente.grid(row=1, column=0, sticky="w", padx=(20, 10))

        self.entry_nome_cliente = CTkEntry(master=self.frame_cima)
        # sticky="ew" (East-West) manda o entry esticar de um lado a outro da coluna
        self.entry_nome_cliente.grid(row=2, column=0, sticky="ew", padx=(20, 10), pady=(0, 15))

        # Solicitante
        self.label_solicitante = CTkLabel(master=self.frame_cima, text="Solicitante:", font=("Arial", 12, "bold"))
        self.label_solicitante.grid(row=1, column=1, sticky="w", padx=(10, 20))

        self.entry_solicitante = CTkEntry(master=self.frame_cima)
        self.entry_solicitante.grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=(0, 15))

        # CC
        self.label_cc = CTkLabel(master=self.frame_cima, text="CC:", font=("Arial", 12, "bold"))
        self.label_cc.grid(row=3, column=0, sticky="w", padx=(20, 10))
        
        self.entry_cc = CTkEntry(master=self.frame_cima)
        self.entry_cc.grid(row=4, column=0, sticky="ew", padx=(20, 10), pady=(0, 20))

        # Matriz
        self.opcoes = ["Água subterrânea", "Água superficial", "Efluente", "Resíduo", "Sedimento", "Solo", "Vapor"]
        self.label_matriz = CTkLabel(master=self.frame_cima, text="Matriz:", font=("Arial", 12, "bold"))
        self.label_matriz.grid(row=3, column=1, sticky="w", padx=(10, 20))

        self.entry_matriz = CTkComboBox(master=self.frame_cima, values=self.opcoes, state="readonly")
        self.entry_matriz.grid(row=4, column=1, sticky="ew", padx=(10, 20), pady=(0, 20))
        self.entry_matriz._entry.bind("<Button-1>", lambda e: self.entry_matriz._clicked())

        self.lista_clientes_completa = self._get_clients_list()