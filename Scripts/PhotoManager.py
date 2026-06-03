import sys
import shutil
import pandas as pd

from pathlib import Path


class PhotoManager:
    def __init__(
        self, list_images: str | Path, excel_ids: str | Path, saida: str | Path
    ):

        self.list_images = Path(list_images)
        self.excel_ids = pd.read_excel(excel_ids, sheet_name="base imagens (valores)")
        self.saida = Path(saida)

        # Diretório raiz: onde o .exe está ou onde o script .py está
        if getattr(sys, "frozen", False):
            self.base_dir = Path(sys.executable).parent
        else:
            self.base_dir = Path(__file__).parent

    def list_photos(self) -> pd.DataFrame:
        """
        Retorna um Dataframe dos nomes dos arquivos do diretório.
        """
        files = [files.name for files in self.list_images.iterdir() if files.is_file()]

        return pd.DataFrame(files, columns=["fulcrum_id_foto"])

    def list_ids(self) -> pd.DataFrame:
        """
        Retorna as colunas relevantes do Excel.
        """
        return self.excel_ids.iloc[:, [3, 4]]

    def rename_photos(self, progress_callback=None) -> bool:
        """
        Cruza os nomes do diretório com o Excel, renomeia/copia os arquivos
        e gera um relatório TXT caso existam arquivos sem correspondência.
        Retorna True se houver pendências, False se tudo bateu com o Excel.
        """
        df_photos = self.list_photos()
        df_excel = self.list_ids()

        # Coluna auxiliar sem extensão para fazer o merge
        df_photos["chave"] = df_photos["fulcrum_id_foto"].apply(lambda x: Path(x).stem)

        # Garante que a chave do Excel também está limpa
        df_excel = df_excel.copy()
        df_excel["chave"] = df_excel["fulcrum_id_foto"].astype(str).str.strip()

        # Filtra os arquivos do diretório cuja 'chave' NÃO está no Excel
        df_sem_correspondencia = df_photos[~df_photos["chave"].isin(df_excel["chave"])]

        # Caso existam arquivos sem correspondência
        tem_nao_correspondidos = False
        txt_path = None

        if not df_sem_correspondencia.empty:
            tem_nao_correspondidos = True

            # Caminho do relatório TXT de inconsistências
            txt_path = self.base_dir / "arquivos_sem_correspondencia.txt"

            # Cria o arquivo TXT contendo os arquivos não encontrados no Excel
            with open(txt_path, "w", encoding="utf-8") as f:

                f.write("=== ARQUIVOS NÃO ENCONTRADOS NO EXCEL ===\n")
                f.write(
                    f"Total de arquivos sem correspondência: "
                    f"{len(df_sem_correspondencia)}\n\n"
                )

                # Escreve o nome de cada arquivo não correspondente
                for nome_arquivo in df_sem_correspondencia["fulcrum_id_foto"]:
                    f.write(f"{nome_arquivo}\n")

        # Realiza o merge entre os arquivos do diretório e os dados do Excel
        df_merged = df_photos.merge(df_excel, on="chave", suffixes=("_dir", "_excel"))

        total = len(df_merged)

        # Percorre cada linha correspondente encontrada
        for i, (_, row) in enumerate(df_merged.iterrows(), start=1):

            # Caminho completo do arquivo original
            arquivo_original = self.list_images / row["fulcrum_id_foto_dir"]

            # Mantém a extensão original do arquivo
            extensao = arquivo_original.suffix

            # Monta o novo nome utilizando o valor do Excel
            new_name = f"{row['nome final imagens']}{extensao}"

            # Caminho final do arquivo renomeado
            arquivo_saida = self.saida / new_name

            # Copia o arquivo para a pasta de saída já com o novo nome
            shutil.copy2(arquivo_original, arquivo_saida)

            # Reporta progresso por arquivo
            if progress_callback:
                progress_callback(i, total)

        # Retorna se houve arquivos sem correspondência
        return {
            "tem_nao_correspondidos": tem_nao_correspondidos,
            "txt_path": str(txt_path) if txt_path else None,
        }
