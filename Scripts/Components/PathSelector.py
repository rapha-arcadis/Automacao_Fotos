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
            master, height=45, corner_radius=8, 
            fg_color=("#FFB786", "#F49A5E"), border_color="#E56011", border_width=2, **kwargs
        )

        self.input_path = None
        self.output_path = None

        # Load Images
        self.icon_up_grey = ctk.CTkImage(light_image=Image.open(resource_path("assets/arrow-circle-up_grey.png")), size=(30, 30))
        self.icon_up_green = ctk.CTkImage(light_image=Image.open(resource_path("assets/arrow-circle-up_green.png")), size=(30, 30))
        self.icon_down_grey = ctk.CTkImage(light_image=Image.open(resource_path("assets/arrow-circle-down_grey.png")), size=(30, 30))
        self.icon_down_green = ctk.CTkImage(light_image=Image.open(resource_path("assets/arrow-circle-down_green.png")), size=(30, 30))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Button (Input File)
        self.btn_left = ctk.CTkButton(
            self, text="Escolher Arquivo", image=self.icon_up_grey, compound="bottom",
            height=100, corner_radius=0, fg_color="transparent", hover_color="#F49A5E",
            text_color="gray14", text_color_disabled="gray14", font=("Arial", 13, "bold"),
            command=self._select_file
        )
        self.btn_left.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)

        # Divider Line
        self.divider = ctk.CTkFrame(self, width=2, height=1, fg_color="#E56011", corner_radius=0)
        self.divider.grid(row=0, column=1, sticky="ns", pady=2)

        # Right Button (Output Directory)
        self.btn_right = ctk.CTkButton(
            self, text="Caminho pasta base", image=self.icon_down_grey, compound="bottom",
            height=100, corner_radius=0, fg_color="transparent", hover_color="#F49A5E",
            text_color="gray14", text_color_disabled="gray14", font=("Arial", 13, "bold"),
            command=self._select_folder
        )
        self.btn_right.grid(row=0, column=2, sticky="nsew", padx=(0, 2), pady=2)

    def _select_file(self):
        path = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Excel", "*.xlsx *.xls *.xlsm")])
        if path:
            self.input_path = path
            self.btn_left.configure(image=self.icon_up_green)

    def _select_folder(self):
        path = filedialog.askdirectory(title="Selecione a pasta para salvar os resultados")
        if path:
            self.output_path = path
            self.btn_right.configure(image=self.icon_down_green)

    def get_paths(self):
        return {"input_path": self.input_path, "base_path": self.output_path}

    def reset(self):
        self.input_path = None
        self.output_path = None
        self.btn_left.configure(image=self.icon_up_grey)
        self.btn_right.configure(image=self.icon_down_grey)

    def lock(self):
        self.btn_left.configure(state="disabled")
        self.btn_right.configure(state="disabled")

    def unlock(self):
        self.btn_left.configure(state="normal")
        self.btn_right.configure(state="normal")