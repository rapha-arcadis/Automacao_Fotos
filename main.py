import os
import sys
import time

# Importa a interface que criamos no arquivo App.py
from App import App


def logica_de_negocio_falsa(**kwargs):
    """
    (MOCK) Simula o processamento de dados.
    Ele finge que está trabalhando por 3 segundos e retorna um caminho de sucesso.
    """

    # Pausa de 3 segundos só para você conseguir ver a barra de progresso animando na tela
    time.sleep(3)

    # Retorna um caminho de mentira para o App tentar "abrir a pasta" no final
    caminho_falso = os.path.abspath("C:/Pasta_Simulada/Resultado.xlsx")
    return caminho_falso


def buscar_dados_iniciais_falsos() -> list:
    """
    (MOCK) Simula uma requisição à API para buscar a lista de clientes.
    Assim o seu ComboBox/Dropdown não fica vazio na hora de testar a tela.
    """

    lista_simulada = [
        "Arcadis Brasil",
        "Vale S.A.",
        "Petrobras",
        "Braskem",
        "Anglo American",
    ]

    return lista_simulada


if __name__ == "__main__":

    # 1. Coleta os dados de mentira (Mocks)
    lista_clientes = buscar_dados_iniciais_falsos()

    # 2. Instancia o App e injeta a função falsa e a lista
    app = App(process_service=logica_de_negocio_falsa, client_list=lista_clientes)

    # 3. Roda a tela para você visualizar!
    app.mainloop()
