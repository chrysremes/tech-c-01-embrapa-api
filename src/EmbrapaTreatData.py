import pandas as pd
import re
from EmbrapaDefs import EmbrapaPages


class EmbrapaData(EmbrapaPages):

    def __init__(self, df:pd.DataFrame, year:int, option:str, suboption:str|None)->None:
        self.df:pd.DataFrame = df
        self.year:int = year
        self.option:str = option
        self.suboption:str = "" if suboption is None else suboption
        self.col_key_name:str = EmbrapaPages.TABLE_HEADERS[option][suboption][0]
        self.col_value_name:list[str] = []
        self.data_main_index_name = "data_"+self.option+"_"+self.suboption
        for index in range(1,len(EmbrapaPages.TABLE_HEADERS[option][suboption])):
            self.col_value_name.append(EmbrapaPages.TABLE_HEADERS[option][suboption][index])
        self.dict_cleaned:dict[str:list] = {self.data_main_index_name : []}
    
    def define_index_total(self):
        return self.df[self.df[self.col_key_name]=="Total"].index

    def remove_total(self, index_total):
        self.df.drop(index_total,inplace=True)

    def check_if_category(self, value:str):
        return value.isupper()

    def format_category(self, value:str):
        return value.lower()

    def check_hifen_value_instead_numeric(self,value):
        if value in ['-','*']:
            return True
    
    def format_numeric_value(self,value):
        return int(re.sub(r'[^\w]','',value))
    
    def get_current_values_list(self,current_col_value_name:list[str]):
        current_quantity:list[int] = []
        for idx in range(0,len(self.col_value_name)):
            if self.check_hifen_value_instead_numeric(current_col_value_name.iloc[idx]):
                current_quantity.append(EmbrapaPages.VALUE_TO_REPLACE_HIFEN)
            else:
                current_quantity.append(self.format_numeric_value(current_col_value_name.iloc[idx]))
        return current_quantity

    def make_new_entry(self, current_category:int, key:str, value:list[int]):
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

    def get_full_data_list(self):
        full_data_list:list = []
        row:dict[str,str]
        current_category:str = ''
        for _, row in self.df.iterrows():
            if self.check_if_category(row[self.col_key_name]):
                current_category = self.format_category(row[self.col_key_name])
            else:
                current_quantity = self.get_current_values_list(row[self.col_value_name])
                full_data_list.append(self.make_new_entry(current_category, self.format_category(row[self.col_key_name]), current_quantity))
        return full_data_list

    def get_cleaned_data_dict(self):
        self.remove_total(self.define_index_total())
        self.dict_cleaned.update({self.data_main_index_name : self.get_full_data_list()})
        return self.dict_cleaned