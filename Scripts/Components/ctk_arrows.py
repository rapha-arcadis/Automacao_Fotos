import customtkinter
from PIL import Image


class Arrows:
    def __init__(self):
        
    # Setas de Upload (Escolher Arquivo)
    self.icone_subir_cinza = customtkinter.CTkImage(
        light_image=Image.open(resource_path("assets/arrow-circle-up_grey.png")), 
        size=(30, 30)
    )
    self.icone_subir_verde = customtkinter.CTkImage(
        light_image=Image.open(resource_path("assets/arrow-circle-up_green.png")), 
        size=(30, 30)
    )

    # Setas de Download/Diretório (Salvar em)
    self.icone_descer_cinza = customtkinter.CTkImage(
        light_image=Image.open(resource_path("assets/arrow-circle-down_grey.png")), 
        size=(30, 30)
    )
    self.icone_descer_verde = customtkinter.CTkImage(
        light_image=Image.open(resource_path("assets/arrow-circle-down_green.png")), 
        size=(30, 30)
    )