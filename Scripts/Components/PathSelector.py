import os
import sys
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class PathSelector(ctk.CTkFrame):
    """Component handling file and directory selections with visual feedback."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            height=45,
            corner_radius=8,
            fg_color=("#E96F23", "#F49A5E"),
            border_color="#E56011",
            border_width=2,
            **kwargs,
        )

        self.input_path = None
        self.excel_path = None
        self.output_path = None

        self.icon_up_grey = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/arrow-circle-up.png")),
            size=(30, 30),
        )
        self.icon_down_grey = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/arrow-circle-down.png")),
            size=(30, 30),
        )

        # ── Grid: 5 colunas (btn | div | btn | div | btn) ───────────
        self.grid_columnconfigure(0, weight=1)  # botão esquerdo
        self.grid_columnconfigure(1, weight=0)  # divisor 1
        self.grid_columnconfigure(2, weight=1)  # botão central
        self.grid_columnconfigure(3, weight=0)  # divisor 2
        self.grid_columnconfigure(4, weight=1)  # botão direito
        self.grid_rowconfigure(0, weight=1)

        self.btn_left = ctk.CTkButton(
            self,
            text="Escolher Diretório",
            image=self.icon_up_grey,
            compound="bottom",
            height=100,
            corner_radius=0,
            fg_color="transparent",
            hover_color="#F49A5E",
            text_color="gray14",
            text_color_disabled="gray14",
            font=("Arial", 13, "bold"),
            command=self._select_file,
        )
        self.btn_left.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=3)

        self.divider1 = ctk.CTkFrame(
            self, width=2, height=1, fg_color="gray70", corner_radius=0
        )
        self.divider1.grid(row=0, column=1, sticky="ns", pady=2)

        self.btn_center = ctk.CTkButton(
            self,
            text="Selecionar Excel",
            image=self.icon_up_grey,
            compound="bottom",
            height=100,
            corner_radius=0,
            fg_color="transparent",
            hover_color="#F49A5E",
            text_color="gray14",
            text_color_disabled="gray14",
            font=("Arial", 13, "bold"),
            command=self._select_excel,
        )
        self.btn_center.grid(row=0, column=2, sticky="nsew", pady=2)

        self.divider2 = ctk.CTkFrame(
            self, width=2, height=1, fg_color="gray70", corner_radius=0
        )
        self.divider2.grid(row=0, column=3, sticky="ns", pady=2)

        self.btn_right = ctk.CTkButton(
            self,
            text="Diretório de saída",
            image=self.icon_down_grey,
            compound="bottom",
            height=100,
            corner_radius=0,
            fg_color="transparent",
            hover_color="#F49A5E",
            text_color="gray14",
            text_color_disabled="gray14",
            font=("Arial", 13, "bold"),
            command=self._select_folder,
        )
        self.btn_right.grid(row=0, column=4, sticky="nsew", padx=(0, 2), pady=2)

    def _select_file(self):
        path = filedialog.askopenfilename(
            title="Selecione o arquivo Excel",
            filetypes=[("Excel", "*.xlsx *.xls *.xlsm")],
        )
        if path:
            self.input_path = path
            self.btn_left.configure(fg_color="#409699")

    def _select_excel(self):
        path = filedialog.askopenfilename(
            title="Selecione o arquivo Excel",
            filetypes=[("Excel", "*.xlsx *.xls *.xlsm")],
        )
        if path:
            self.excel_path = path
            self.btn_center.configure(fg_color="#409699")

    def _select_folder(self):
        path = filedialog.askdirectory(
            title="Selecione a pasta para salvar os resultados"
        )
        if path:
            self.output_path = path
            self.btn_right.configure(fg_color="#409699")

    def get_paths(self):
        return {
            "input_path": self.input_path,
            "excel_path": self.excel_path,
            "base_path": self.output_path,
        }

    def reset(self):
        self.input_path = None
        self.excel_path = None
        self.output_path = None
        self.btn_left.configure(image=self.icon_up_grey, fg_color="transparent")
        self.btn_center.configure(image=self.icon_up_grey, fg_color="transparent")
        self.btn_right.configure(image=self.icon_down_grey, fg_color="transparent")

    def lock(self):
        self.btn_left.configure(state="disabled")
        self.btn_center.configure(state="disabled")
        self.btn_right.configure(state="disabled")

    def unlock(self):
        self.btn_left.configure(state="normal")
        self.btn_center.configure(state="normal")
        self.btn_right.configure(state="normal")
