import requests
import bs4
import pandas as pd
from io import StringIO
from fastapi import HTTPException

from EmbrapaDefs import EmbrapaPages

class EmbrapaWebScrap(EmbrapaPages):

    def __init__(self, year:int, option:str, suboption:str)->None:
        self.year = year
        self.option:str = option
        self.suboption:str = suboption
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
        else:
            pass # do nothing (everything is ok, passed)
    
    def check_valid_options(self)->None:
        valid_options:tuple[str] = self.get_all_valid_options()
        if self.option not in (valid_options):
            raise HTTPException(status_code=404, detail=f"Not Found: 'option' argument should be one of the valid options: {valid_options}.")
            raise Exception(f"'option' argument should be one of the valid options: {valid_options}.")
        else:
            pass # do nothing (everything is ok, passed)
    
    def check_valid_suboptions(self)->None:
        if self.option in ("processamento","importacao","exportacao"):
            valid_suboptions:tuple[str] = self.get_all_valid_suboptions(self.option)
            if self.suboption not in (valid_suboptions):
                raise HTTPException(status_code=404, detail=f"Not Found: 'suboption' argument should be one of the valid options: {valid_suboptions} for option={self.option}.")
                raise Exception(f"'suboption' argument should be one of the valid options: {valid_suboptions} for option={self.option}.")
            else:
                pass # do nothing (everything is ok, passed)
        else:
            if self.suboption is not None:
                raise HTTPException(status_code=404, detail=f"Not Found: 'suboption' argument should be 'None' for this page (there is no suboption here).")
                raise Exception(f"'suboption' argument should be 'None' for this page (there is no suboption here).")
            else:
                pass # do nothing (everything is ok, passed)
    
    def check_valid_year(self)->None:
        if (self.year not in range(self.START_YEAR, self.LAST_YEAR+1, 1)):
                raise HTTPException(status_code=404, detail=f"Not Found: Year parameters should be in a valid range, from {self.START_YEAR} to {self.LAST_YEAR}.")
                raise Exception(f"Not Found: Year parameters should be in a valid range, from {self.START_YEAR} to {self.LAST_YEAR}.")
        else:
            pass # do nothing (everything is ok, passed)

    def parse_url(self)->str:
        if self.option in ("processamento","importacao","exportacao"):
            url_request = self.URL_INDEX+self.REQ_YEAR+str(self.year)+"&"+self.REQ_SUBOPTION+self.SUBOPTIONS_DICT[self.option][self.suboption]+"&"+self.REQ_OPTION+self.OPTIONS_DICT[self.option]
        else:
            url_request = self.URL_INDEX+self.REQ_YEAR+str(self.year)+"&"+self.REQ_OPTION+self.OPTIONS_DICT[self.option]
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
        self.check_valid_year()
        self.url_request = self.parse_url()
        print(self.url_request)
        self.df = self.request_to_df(self.url_request)
        print(self.df.head())

