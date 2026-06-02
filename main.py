import customtkinter as ctk

# Importa a interface diretamente da raiz
from App import App 

from Scripts.PhotoManager import PhotoManager
from Scripts.VideoManager import VideoManager 

def orquestrador_de_processamento(input_path, excel_path, base_path, tipo_conversao, progress_callback=None):
    """
    Controla o fluxo de dados entre a Interface e as Regras de Negócio.
    """
    try:
        if progress_callback:
            progress_callback(0.1, f"Iniciando conversão de {tipo_conversao}...")

        # Instancia a classe correta baseada no ComboBox
        if tipo_conversao == "Imagens":
            manager = PhotoManager(input_path, excel_path, base_path)
            
            if progress_callback:
                progress_callback(0.4, "Lendo fotos e cruzando com o Excel...")
            
            manager.rename_photos()
            
        elif tipo_conversao == "Videos":
            manager = VideoManager(input_path, excel_path, base_path)
            
            if progress_callback:
                progress_callback(0.4, "Lendo vídeos e cruzando com o Excel...")
                
            manager.rename_videos()
        
        else:
            raise ValueError("Tipo de conversão desconhecido!")

        if progress_callback:
            progress_callback(1.0, "Processamento concluído com sucesso!")

        return base_path

    except Exception as e:
        raise Exception(f"Falha ao processar {tipo_conversao}: {str(e)}")

if __name__ == "__main__":
    # Inicia o App injetando apenas o serviço
    app = App(process_service=orquestrador_de_processamento)
    app.mainloop()