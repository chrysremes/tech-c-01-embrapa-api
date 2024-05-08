import requests
import bs4
import pandas as pd
from io import StringIO
from fastapi import HTTPException

from EmbrapaDefs import EmbrapaPages

class EmbrapaWebScrap(EmbrapaPages):
    """
    This class has everything needed to WebScrap Embrapa webpage.
    """

    def __init__(self, year:int, option:str, suboption:str)->None:
        """
        Instantiating/Initializating the class.
        """
        self.year = year
        self.option:str = option
        self.suboption:str = suboption
        self.url_request:str = None
        self.df:pd.DataFrame = None
        self.df_as_dict:dict = None
        self.df_as_csv:dict = None
        
    def get_all_valid_options(self)->tuple[str]:
        """
        Returns all the possible 'option' values.
        """
        return tuple(self.OPTIONS_DICT.keys())
    
    def get_all_valid_suboptions(self,option:str)->tuple[str]:
        """
        Returns all the possible 'suboption' values for a given 'option'.
        """
        return tuple(self.SUBOPTIONS_DICT[option].keys())

    def check_null_args(self)->None:
        """
        Check if 'option' is None (no option was passed on the API request)
        """
        if self.option is None:
            raise HTTPException(status_code=404, detail=f"Not Found: 'option' argument cannot be 'None' (empty) when instancing this class.")
            raise Exception("'option' argument cannot be 'None' (empty) when instancing this class.")
        else:
            pass # do nothing (everything is ok, passed)
    
    def check_valid_options(self)->None:
        """
        Checks if provided option on API request is within valid options.
        """
        valid_options:tuple[str] = self.get_all_valid_options()
        if self.option not in (valid_options):
            raise HTTPException(status_code=404, detail=f"Not Found: 'option' argument should be one of the valid options: {valid_options}.")
            raise Exception(f"'option' argument should be one of the valid options: {valid_options}.")
        else:
            pass # do nothing (everything is ok, passed)
    
    def check_valid_suboptions(self)->None:
        """
        Checks if provided suboption on API request is within valid suboptions, given the corresponding option.
        """
        # Checking if the suboption from API request is within the valid set for the corresponding option.
        if self.option in ("processamento","importacao","exportacao"):
            valid_suboptions:tuple[str] = self.get_all_valid_suboptions(self.option)
            if self.suboption not in (valid_suboptions):
                raise HTTPException(status_code=404, detail=f"Not Found: 'suboption' argument should be one of the valid options: {valid_suboptions} for option={self.option}.")
                raise Exception(f"'suboption' argument should be one of the valid options: {valid_suboptions} for option={self.option}.")
            else:
                pass # do nothing (everything is ok, passed)
        # These options do not have corresponding suboption (suboption MUST be None)
        else:
            if self.suboption is not None:
                raise HTTPException(status_code=404, detail=f"Not Found: 'suboption' argument should be 'None' for this page (there is no suboption here).")
                raise Exception(f"'suboption' argument should be 'None' for this page (there is no suboption here).")
            else:
                pass # do nothing (everything is ok, passed)
    
    def check_valid_year(self)->None:
        """
        Make a validity test for the input year value. Should be within [START_YEAR,LAST_YEAR].
        """
        if (self.year not in range(self.START_YEAR, self.LAST_YEAR+1, 1)):
                raise HTTPException(status_code=404, detail=f"Not Found: Year parameters should be in a valid range, from {self.START_YEAR} to {self.LAST_YEAR}.")
                raise Exception(f"Not Found: Year parameters should be in a valid range, from {self.START_YEAR} to {self.LAST_YEAR}.")
        else:
            pass # do nothing (everything is ok, passed)

    def parse_url(self)->str:
        """
        Creates a suitable string representing the URL for requesting data to Embrapa Website.
        Example: considering year=2020, option=processamento, suboption=viniferas
        the URL string after correct parsing should be 
        http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2020&opcao=opt_03&subopcao=subopt_01
        Notice that for some options, there is no suboption.
        Example 2: considering year=2020, option=producao (and suboption=None)
        then http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2020&opcao=opt_02
        """

        if self.option in ("processamento","importacao","exportacao"):
            url_request = self.URL_INDEX+self.REQ_YEAR+str(self.year)+"&"+self.REQ_SUBOPTION+self.SUBOPTIONS_DICT[self.option][self.suboption]+"&"+self.REQ_OPTION+self.OPTIONS_DICT[self.option]
        else:
            url_request = self.URL_INDEX+self.REQ_YEAR+str(self.year)+"&"+self.REQ_OPTION+self.OPTIONS_DICT[self.option]
        return (url_request)

    def request_to_df(self,url:str):
        """
        Given the parsed URL, this method makes the Web Scraping of the page.
        The Scrap is configured to extract just the table of the page (which is the part that contains the data)
        """
        request = requests.get(url)
        soup = bs4.BeautifulSoup(request.text,"lxml")
        table = soup.find('table', attrs={'class':'tb_base tb_dados'})
        return (pd.read_html(StringIO(str(table)))[0])

    def request_and_save_to_df(self)->None:
        """
        This method calls all the needed checks and does the web scraping after.
        The data is converted to a Pandas DF before being stored on the attribute 'df' of this class.
        """
        self.check_null_args()
        self.check_valid_options()
        self.check_valid_suboptions()
        self.check_valid_year()
        self.url_request = self.parse_url()
        print(self.url_request)
        self.df = self.request_to_df(self.url_request)
        print("###### End of WebScrapping ##########")

