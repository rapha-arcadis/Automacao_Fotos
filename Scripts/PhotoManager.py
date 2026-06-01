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
        # self.saida.mkdir(parents=True, exist_ok=True)  # cria a pasta de saída se não existir

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

    def rename_photos(self) -> pd.DataFrame:
        """
        Cruza os nomes do diretório com o Excel e renomeia/copia os arquivos
        para a pasta de saída.
        """
        df_photos = self.list_photos()
        df_excel = self.list_ids()

        # Coluna auxiliar sem extensão para fazer o merge
        df_photos["chave"] = df_photos["fulcrum_id_foto"].apply(lambda x: Path(x).stem)

        # Garante que a chave do Excel também está limpa
        df_excel = df_excel.copy()
        df_excel["chave"] = df_excel["fulcrum_id_foto"].astype(str).str.strip()

        # Merge pela chave (inner = só os que existem nos dois lados)
        df_merged = df_photos.merge(df_excel, on="chave", suffixes=("_dir", "_excel"))

        # Renomeia e copia para a saída
        for _, row in df_merged.iterrows():

            arquivo_original = self.list_images / row["fulcrum_id_foto_dir"]
            extensao = arquivo_original.suffix  # Preserva a extensão original

            new_name = f"{row['nome final imagens']}{extensao}"
            arquivo_saida = self.saida / new_name

            shutil.copy2(arquivo_original, arquivo_saida)

        # return df_resultado
