import requests
import bs4
import pandas as pd
from io import StringIO
from fastapi import HTTPException

class EmbrapaPages():

    URL_INDEX = "http://vitibrasil.cnpuv.embrapa.br/index.php?"

    REQ_OPTION = "opcao=opt_"
    REQ_SUBOPTION = "subopcao=subopt_"

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

class EmbrapaURL(EmbrapaPages):

    def __init__(self, option:str, suboption:str|None=None)->None:
        self.option:str = option
        self.suboption:str|None = suboption
        self.url_request:str = None
        self.df:pd.DataFrame = None
        self.df_as_dict:dict = None
        self.df_as_csv:dict = None
        
    def get_all_valid_options(self)->tuple[str]:
        return tuple(self.OPTIONS_DICT.keys())
    
    def get_all_valid_suboptions(self,option_to_check:str)->tuple[str]:
        return tuple(self.SUBOPTIONS_DICT[option_to_check].keys())

    def check_null_args(self)->None:
        if self.option is None:
            raise HTTPException(status_code=404, detail=f"Not Found: 'option' argument cannot be 'None' (empty) when instancing this class.")
            raise Exception("'option' argument cannot be 'None' (empty) when instancing this class.")
    
    def check_valid_options(self)->None:
        valid_options:tuple[str] = self.get_all_valid_options()
        if self.option not in (valid_options):
            raise HTTPException(status_code=404, detail=f"Not Found: 'option' argument should be one of the valid options: {valid_options}.")
            raise Exception(f"'option' argument should be one of the valid options: {valid_options}.")
    
    def check_valid_suboptions(self)->None:
        if self.option in ("processamento","importacao","exportacao"):
            valid_suboptions:tuple[str] = self.get_all_valid_suboptions(self.option)
            if self.suboption not in (valid_suboptions):
                raise HTTPException(status_code=404, detail=f"Not Found: 'suboption' argument should be one of the valid options: {valid_suboptions} for option={self.option}.")
                raise Exception(f"'suboption' argument should be one of the valid options: {valid_suboptions} for option={self.option}.")
        else:
            if self.suboption is not None:
                raise HTTPException(status_code=404, detail=f"Not Found: 'suboption' argument should be 'None' for this page (there is no suboption here).")
                raise Exception(f"'suboption' argument should be 'None' for this page (there is no suboption here).")
    
    def parse_url(self)->str:
        if self.option in ("processamento","importacao","exportacao"):
            url_request = self.URL_INDEX+self.REQ_SUBOPTION+self.SUBOPTIONS_DICT[self.option][self.suboption]+"&"+self.REQ_OPTION+self.OPTIONS_DICT[self.option]
        else:
            url_request = self.URL_INDEX+self.REQ_OPTION+self.OPTIONS_DICT[self.option]
        return (url_request)

    def request_to_df(self,url:str):
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text,"lxml")
        table = soup.find('table', attrs={'class':'tb_base tb_dados'})
        return (pd.read_html(StringIO(str(table)))[0])

    def request_and_save_to_df(self)->None:
        self.check_null_args()
        self.check_valid_options()
        self.check_valid_suboptions()
        self.url_request = self.parse_url()
        print(self.url_request)
        self.df = self.request_to_df(self.url_request)
        print(self.df.head())

