# Automação renomear arquivos

Ferramenta desktop para renomeação em lote e correspondência de arquivos de mídia (imagens e vídeos) com base em dados de planilhas, desenvolvida em Python utilizando CustomTkinter e Pandas.

---

## Funcionamento

* O usuário inicia a aplicação.
* Pela interface gráfica, o usuário seleciona:
  * O diretório contendo os arquivos de mídia originais;
  * A planilha Excel com as regras de renomeação;
  * A pasta de destino onde os arquivos processados serão salvos.

* Em seguida, o usuário escolhe o tipo de mídia a ser processado:
  * Imagens; ou
  * Vídeos.

* O usuário inicia o processamento.
* Durante o processamento, o andamento é exibido por meio de uma barra de progresso.
* O sistema cruza os nomes dos arquivos originais com os IDs existentes na planilha Excel.
* Para os arquivos com correspondência encontrada:
  * O sistema copia os arquivos;
  * Renomeia os arquivos conforme as regras da planilha;
  * Salva os arquivos processados na pasta de saída selecionada.
  
* Ao final do processamento, o sistema abre automaticamente o diretório de destino.
* Caso existam arquivos originais sem correspondência na base de dados, o sistema gera um arquivo de texto contendo o relatório dessas inconsistências.

---

## Estrutura do Projeto

```text
Automacao_Fotos/
├── App.py                  # Orquestrador principal da interface gráfica e gerenciamento de estado
├── main.py                 # Ponto de entrada da aplicação e orquestrador das regras de negócio
├── Scripts/                # Componentes modulares da interface e outras utilidades
│   ├── PhotoManager.py         # Lógica de cruzamento de dados e renomeação específica para imagens
│   ├── VideoManager.py         # Lógica de cruzamento de dados e renomeação específica para vídeos
└── assets/                 # Recursos visuais como ícones e temas

```

---

## Requisitos

**Python 3.12+**

Dependências:

* *pandas* : manipulação e cruzamento de DataFrames
* *customtkinter* : interface gráfica moderna baseada em Tkinter
* *Pillow* : carregamento de imagens na GUI

---

## Configuração do Ambiente

### 1. Clonar o repositório e acessar o diretório

```bash
git clone https://github.com/rapha-arcadis/Automacao_Fotos
cd Automacao_Fotos
```

### 2. Criação do ambiente virtual

**Windows:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalação de dependências

```bash
pip install -r requirements.txt
```

---

## App.py — Orquestrador da Interface Gráfica

Gerencia a construção da interface utilizando CustomTkinter, isolando a visualização da lógica de negócios e delegando o processamento pesado para threads secundárias.

### Validação e Submissão

```python
def validate_and_submit(self):
    paths = self.path_selector.get_paths()
    form_data = self.client_form.get_data()
    # (validações omitidas para brevidade)
    thread = threading.Thread(
        target=self._run_service_in_background, args=(kwargs_etl,), daemon=True
    )
    thread.start()
    self._monitor_thread(thread)
```

Coleta os caminhos selecionados pelo usuário, valida o preenchimento, bloqueia a interface e dispara o serviço ETL em uma thread em background para evitar o congelamento da UI.

### Atualização de Progresso

```python
def atualizar_progresso_real(self, valor, texto=None):
    self.after(0, self._apply_progress_update, valor, texto)
```

Recebe as atualizações da thread de processamento e agenda a modificação visual na thread principal utilizando o método `after`, garantindo a segurança de manipulação dos widgets.

---

## main.py — Ponto de Entrada e Orquestração

Atua como ponte entre a interface gráfica e as classes gerenciadoras, instanciando os serviços adequados com base no tipo de conversão selecionado.

### Orquestrador de Processamento

```python
def orquestrador_de_processamento(
    input_path, excel_path, base_path, tipo_conversao, progress_callback=None
):
    # (setup inicial omitido)
    if tipo_conversao == "Imagens":
        manager = PhotoManager(input_path, excel_path, base_path)
        resultado_manager = manager.rename_photos(progress_callback=file_progress)
    # (retorno estruturado omitido)
```

Recebe os parâmetros da UI, instancia as lógicas de negócio (`PhotoManager` ou `VideoManager`) e converte o callback contínuo de progresso em atualizações fracionadas por arquivo, devolvendo os resultados de execução ao final.

---

## PhotoManager.py — Gerenciamento de Imagens

Responsável por ler o diretório de imagens, cruzar com a aba correspondente na planilha Excel e realizar a cópia renomeada dos arquivos.

### Renomeação de Fotos

```python
def rename_photos(self, progress_callback=None) -> bool:
    df_merged = df_photos.merge(df_excel, on="chave", suffixes=("_dir", "_excel"))
  
    for i, (_, row) in enumerate(df_merged.iterrows(), start=1):
        arquivo_original = self.list_images / row["fulcrum_id_foto_dir"]
        new_name = f"{row['nome final imagens']}{arquivo_original.suffix}"
        arquivo_saida = self.saida / new_name
        shutil.copy2(arquivo_original, arquivo_saida)
```

Utiliza a biblioteca pandas para cruzar os dados dos arquivos físicos com a planilha e a biblioteca shutil para realizar a cópia segura para o novo diretório aplicando as regras de nomenclatura atualizadas.

---

## VideoManager.py — Gerenciamento de Vídeos

Possui estrutura semelhante ao PhotoManager, mas configurado com direcionamento para acesso e cruzamento da aba dedicada a vídeos no arquivo Excel.

### Renomeação de Vídeos

```python
def rename_videos(self, progress_callback=None) -> bool:
    df_merged = df_videos.merge(df_excel, on="chave", suffixes=("_dir", "_excel"))
  
    for i, (_, row) in enumerate(df_merged.iterrows(), start=1):
        arquivo_original = self.list_video / row["fulcrum_id_video_dir"]
        new_name = f"{row['nome final videos']}{arquivo_original.suffix}"
        arquivo_saida = self.saida / new_name
        shutil.copy2(arquivo_original, arquivo_saida)
```

Mapeia os vídeos no diretório de entrada, localiza os nomes na planilha através de um cruzamento exato das chaves de identificação limpas, e realiza as cópias mantendo as extensões originais e reportando o progresso de execução.

---
