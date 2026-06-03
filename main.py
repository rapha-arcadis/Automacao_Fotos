import customtkinter as ctk

# Importa a interface diretamente da raiz
from App import App

from Scripts.PhotoManager import PhotoManager
from Scripts.VideoManager import VideoManager


def orquestrador_de_processamento(
    input_path, excel_path, base_path, tipo_conversao, progress_callback=None
):
    try:
        if progress_callback:
            progress_callback(0.05, f"Iniciando conversão de {tipo_conversao}...")

        tem_nao_correspondidos = False

        # Faixa reservada para o processamento pesado: 0.10 → 0.95
        PROGRESS_START = 0.10
        PROGRESS_END = 0.95

        def file_progress(current, total):
            """
            Callback por arquivo - distribui o progresso na faixa reservada.
            """
            if progress_callback and total > 0:
                ratio = current / total
                valor = PROGRESS_START + (PROGRESS_END - PROGRESS_START) * ratio
                progress_callback(valor, f"Processando arquivo {current} de {total}...")

        if tipo_conversao == "Imagens":
            manager = PhotoManager(input_path, excel_path, base_path)
            if progress_callback:
                progress_callback(
                    PROGRESS_START, "Analisando imagens e cruzando dados..."
                )
            tem_nao_correspondidos = manager.rename_photos(
                progress_callback=file_progress
            )

        elif tipo_conversao == "Videos":
            manager = VideoManager(input_path, excel_path, base_path)
            if progress_callback:
                progress_callback(
                    PROGRESS_START, "Analisando vídeos e cruzando dados..."
                )
            tem_nao_correspondidos = manager.rename_videos(
                progress_callback=file_progress
            )

        else:
            raise ValueError("Tipo de conversão desconhecido!")

        if progress_callback:
            progress_callback(1.0, "Processamento finalizado.")

        return {
            "base_path": base_path,
            "tem_nao_correspondidos": tem_nao_correspondidos,
        }

    except Exception as e:
        raise Exception(f"Falha ao processar {tipo_conversao}: {str(e)}")


if __name__ == "__main__":
    # Inicia o App injetando apenas o serviço
    app = App(process_service=orquestrador_de_processamento)
    app.mainloop()
