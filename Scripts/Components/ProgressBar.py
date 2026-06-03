import customtkinter


class ProgressBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._current_value = 0.0
        self._target_value = 0.0
        self._animation_id = None
        self._step = 0.015  # incremento por frame
        self._interval_ms = 25  # ms entre frames (~40 fps)

        self.status_label = customtkinter.CTkLabel(
            self,
            text="Aguardando arquivos...",
            font=("FS Elliot Pro", 12, "bold"),
            text_color="gray60",
        )
        self.status_label.pack(anchor="w")

        self.progressbar = customtkinter.CTkProgressBar(
            self, height=10, progress_color="#E4610F"
        )
        self.progressbar.pack(fill="x")
        self.progressbar.set(0)

    def update_progress(self, target_value):
        """
        Define o valor-alvo e inicia a animação suave até ele.
        """
        self._target_value = min(max(target_value, 0.0), 1.0)
        # Só inicia o loop se não tiver um rodando
        if self._animation_id is None:
            self._animate()

    def _animate(self):
        """
        Loop interno: incrementa a barra até alcançar o target.
        """
        if self._current_value < self._target_value:
            # Calcula o passo dinâmico (mais rápido perto do alvo)
            remaining = self._target_value - self._current_value
            step = max(self._step, remaining * 0.08)

            self._current_value = min(
                self._current_value + step,
                self._target_value,
            )
            self.progressbar.set(self._current_value)
            self._animation_id = self.after(self._interval_ms, self._animate)
        else:
            # Garante o valor exato no final e para o loop
            self._current_value = self._target_value
            self.progressbar.set(self._current_value)
            self._animation_id = None

    def _cancel_animation(self):
        """
        Cancela qualquer animação pendente.
        """
        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None

    def set_processing(self):
        self._cancel_animation()
        self._current_value = 0.0
        self._target_value = 0.0
        self.progressbar.set(0)
        self.status_label.configure(
            text="Lendo e formatando dados...",
            text_color="#E4610F",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def set_success(self):
        self._cancel_animation()
        self._current_value = 1.0
        self.progressbar.set(1)
        self.status_label.configure(
            text="Concluído com sucesso!",
            text_color="green",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def set_file_open(self):
        self._cancel_animation()
        self._current_value = 0.0
        self.progressbar.set(0)
        self.status_label.configure(
            text="Operação cancelada (Arquivo em uso).",
            text_color="red",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def set_error(self):
        self._cancel_animation()
        self._current_value = 0.0
        self.progressbar.set(0)
        self.status_label.configure(
            text="Erro no processamento.",
            text_color="red",
            font=("FS Elliot Pro", 12, "bold"),
        )

    def reset(self):
        self._cancel_animation()
        self._current_value = 0.0
        self._target_value = 0.0
        self.progressbar.set(0)
        self.status_label.configure(
            text="Aguardando arquivo...",
            text_color="gray60",
            font=("FS Elliot Pro", 12, "bold"),
        )
