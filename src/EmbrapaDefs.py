from pydantic import BaseModel
from enum import Enum

class EmbrapaPages():

    URL_INDEX = "http://vitibrasil.cnpuv.embrapa.br/index.php?"

    REQ_YEAR = "ano="
    REQ_OPTION = "opcao=opt_"
    REQ_SUBOPTION = "subopcao=subopt_"

    START_YEAR = 1970
    LAST_YEAR = 2022

    LIT_PRODUTO = "Produto"
    LIT_QUANTIDADE_L = "Quantidade (L.)"
    LIT_CULTIVAR = "Cultivar"
    LIT_QUANTIDADE_KG = "Quantidade (Kg)"
    LIT_SEM_DEF = "Sem definição"
    LIT_PAISES = "Países"
    LIT_VALOR = "Valor (US$)"

    OPTIONS_DICT = {
        "producao" : "02",
        "processamento" : "03",
        "comercializacao" : "04",
        "importacao" : "05",
        "exportacao" : "06"
    }

    SUBOPTIONS_DICT = {
        "processamento" : {
            "viniferas" : "01",
            "americanas_e_hibridas" : "02",
            "uvas_de_mesa" : "03",
            "sem_classificacao" : "04"
        },
        "importacao" : {
            "vinhos_de_mesa" : "01",
            "espumantes" : "02",
            "uvas_frescas" : "03",
            "uvas_passas" : "04",
            "suco_de_uva" : "05"
        },
        "exportacao" : {
            "vinhos_de_mesa" : "01",
            "espumantes" : "02",
            "uvas_frescas" : "03",
            "suco_de_uva" : "04"
        }
    }

    TABLE_HEADERS = {
        "producao" : {
            None : [LIT_PRODUTO, LIT_QUANTIDADE_L]
        },
        "processamento" : {
            "viniferas" : [LIT_CULTIVAR, LIT_QUANTIDADE_KG],
            "americanas_e_hibridas" : [LIT_CULTIVAR, LIT_QUANTIDADE_KG],
            "uvas_de_mesa" : [LIT_CULTIVAR, LIT_QUANTIDADE_KG],
            "sem_classificacao" : [LIT_SEM_DEF, LIT_QUANTIDADE_KG]
        },
        "comercializacao" : {
            None : [LIT_PRODUTO, LIT_QUANTIDADE_L]
        },
        "importacao" : {
            "vinhos_de_mesa" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "espumantes" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "uvas_frescas" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "uvas_passas" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "suco_de_uva" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
        },
        "exportacao" : {
            "vinhos_de_mesa" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "espumantes" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "uvas_frescas" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
            "suco_de_uva" : [LIT_PAISES, LIT_QUANTIDADE_KG, LIT_VALOR],
        }
    }

class DataOption(str, Enum):
    producao = "producao"
    processamento = "processamento"
    comercializacao = "comercializacao"
    importacao = "importacao"
    exportacao = "exportacao"

class DataSubOption(str, Enum):
    StrNone = "None"
    processamento_viniferas = "viniferas"
    processamento_americanas_e_hibridas = "americanas_e_hibridas"
    processamento_uvas_de_mesa = "uvas_de_mesa"
    processamento_sem_classificacao = "sem_classificacao"
    importacao_vinhos_de_mesa = "vinhos_de_mesa"
    importacao_espumantes = "espumantes"
    importacao_uvas_frescas = "uvas_frescas"
    importacao_uvas_passas = "uvas_passas"
    importacao_suco_de_uva = "suco_de_uva"
    exportacao_vinhos_de_mesa = "vinhos_de_mesa"
    exportacao_espumantes = "espumantes"
    exportacao_uvas_frescas = "uvas_frescas"
    exportacao_suco_de_uva = "suco_de_uva"

class DataTypeReturn(str, Enum):
    url = "url"
    df_str = "df_str"
    df_csv = "df_csv"
    df_dict = "df_dict"
    df_json = "df_json"
    df_html_tab = "df_html_tab"

