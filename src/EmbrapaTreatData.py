import pandas as pd
import re
from EmbrapaDefs import EmbrapaPages


class EmbrapaData(EmbrapaPages):
    """
    This class has everything needed to treat/clean data scraped from Embrapa Webpage.
    """

    def __init__(self, df:pd.DataFrame, year:int, option:str, suboption:str|None)->None:
        """
        Instantiating/Initializating the class.
        """

        # dataframe with raw data scraped
        self.df:pd.DataFrame = df
        
        # year, option and suboption provided during the web scrap request (suboption converted to str again)
        self.year:int = year
        self.option:str = option
        self.suboption:str = "" if suboption is None else suboption

        # col_key_name has the name of the first column header from the corresponding website page
        # col_value_name has the remaining column names. Initialized as an empty list.
        # Example: for option = "importacao" and suboption = "vinhos_de_mesa"
        # We have a table with columns [ Países | Quantidade (Kg) | Valor (US$)]
        # Then: 
        # col_key_name = "Países"
        # col_value_name = ["Quantidade (Kg)", "Valor (US$)"]
        self.col_key_name:str = EmbrapaPages.TABLE_HEADERS[option][suboption][0]
        self.col_value_name:list[str] = []

        # fill the list with the remaining column names
        for index in range(1,len(EmbrapaPages.TABLE_HEADERS[option][suboption])):
            self.col_value_name.append(EmbrapaPages.TABLE_HEADERS[option][suboption][index])

        # data_main_index_name is just stored to identify the year/option/suboption set used for data gathering
        self.data_main_index_name:str = "data_"+self.option+"_"+self.suboption

        # Initialize the cleaned/treated dict to be returned
        self.dict_cleaned:dict[str:list] = {self.data_main_index_name : []}
    
    def define_index_total(self)-> pd.Index:
        """
        Get the index related to the row "Total" (to be dropped)
        """
        return self.df[self.df[self.col_key_name]=="Total"].index

    def remove_total(self, index_total:pd.Index)->None:
        """
        Drop the row "Total" (can be infered later by sum, for example).
        Having it may complicate data treatment, so it is removed for simplicity.
        """
        self.df.drop(index_total,inplace=True)

    def check_if_category(self, value:str)->bool:
        """
        The table has some rows used to define categories.
        Such rows always have keys in UPPERCASE.
        This method identifies this pattern.
        """
        return value.isupper()

    def format_category(self, value:str)->str:
        """
        Just transform the category string to lowercase to store it later.
        """
        return value.lower()

    def check_hifen_value_instead_numeric(self,value:str)->bool:
        """
        When Scraping the page, some NULL values are filled with 
        either '-' or '*'. This method checks for them.
        """
        if value in ['-','*']:
            return True
        else:
            return False
    
    def format_numeric_value(self,value:str)->int:
        """
        All numeric raw values come as a string with dots, like: 12.345.678
        This method removes non-numeric values and returns the result as an int.
        """
        return int(re.sub(r'[^\w]','',value))
    
    def get_current_values_list(self,current_col_value_name:list[str])->list[int]:
        """
        current_quantity is a list of int values (i.e. numerical)
        that are retrieved from all valued columns for a given year/option/suboption.
        Example: for option = "importacao" and suboption = "vinhos_de_mesa"
        We have a table with columns [ Países | Quantidade (Kg) | Valor (US$)]
        where "Países" is the key column and "Quantidade (Kg)" | "Valor (US$)" are columns with values
        to be stored in current_quantity. Thus, e.g., current_quantity = [12345 0]
        """
        current_quantity:list[int] = []
        for idx in range(0,len(self.col_value_name)):
            # if the value is either '*' or '-', replace with VALUE_TO_REPLACE_HIFEN and append
            if self.check_hifen_value_instead_numeric(current_col_value_name.iloc[idx]):
                current_quantity.append(EmbrapaPages.VALUE_TO_REPLACE_HIFEN)
            # just append the formated value
            else:
                current_quantity.append(self.format_numeric_value(current_col_value_name.iloc[idx]))
        return current_quantity

    def make_new_entry(self, current_category:int, key:str, value:list[int])->dict:
        """
        This is the format a all the entries of the cleaned dict to be returned.
        Notice that suboption is again converted to None, if applicable (instead of empty string "").
        """
        return ({
            'option' : self.option,
            'suboption' : None if self.suboption == "" else self.suboption,
            'col_key_name' : self.col_key_name,
            'col_value_name' : self.col_value_name,
            'category' : current_category,
            'key' : key,
            'value' : value,
            'ano' : self.year
        })

    def get_full_data_list(self)->list[dict]:
        """
        Iterate on the entire raw DataFrame through iterrows.
        For each row, check if it is a category (UPPER),
        or if it is a plain value row to be stored.
        Return a list of dicts as in method self.make_new_entry
        """

        # Initialization
        full_data_list:list = []
        row:dict[str,str]
        current_category:str = ''
        
        for _, row in self.df.iterrows():
            # Check if category: if yes, get its name and use it from now on
            if self.check_if_category(row[self.col_key_name]):
                current_category = self.format_category(row[self.col_key_name])
            # Get and store the values of all columns
            else:
                current_quantity = self.get_current_values_list(row[self.col_value_name])
                full_data_list.append(self.make_new_entry(current_category, self.format_category(row[self.col_key_name]), current_quantity))
        return full_data_list

    def get_cleaned_data_dict(self)->dict[str:list]:
        """
        This method calls all the needed checks and data cleaning routines.
        A cleaned dict is returned, ready to be stored as a json file.
        """
        
        # remove the "Total" row
        self.remove_total(self.define_index_total())
        # store the cleaned data as a list of dicts into self.dict_cleaned and return it
        self.dict_cleaned.update({self.data_main_index_name : self.get_full_data_list()})
        return self.dict_cleaned