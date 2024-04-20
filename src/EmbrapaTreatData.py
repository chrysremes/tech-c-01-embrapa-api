import pandas as pd
import re
from EmbrapaDefs import EmbrapaPages


class EmbrapaData(EmbrapaPages):

    def __init__(self, df:pd.DataFrame, year:int)->None:
        self.df:pd.DataFrame = df
        self.year:int = year
        self.dict_producao_clean:dict[str:list] = {"data_producao" : []}
    
    def define_index_total(self):
        return self.df[self.df["Produto"]=="Total"].index

    def remove_total(self, index_total):
        self.df.drop(index_total,inplace=True)

    def check_if_category(self, value:str):
        return value.isupper()

    def format_category(self, value:str):
        return value.lower()

    def check_hifen_value_instead_numeric(self,value):
        if value == '-':
            return True
    
    def format_numeric_value(self,value):
        return int(re.sub(r'[^\w]','',value))
    
    def make_new_entry_produto(self, current_category:int, produto:str, current_quantity:int, year:int):
        return ({
            'category' : current_category,
            'produto' : produto,
            'quantidade_L' : current_quantity,
            'ano' : year
        })

    def make_dict_producao(self):
        self.remove_total(self.define_index_total())
        data_list:list = []
        row:dict[str,str]
        current_category:str = ''
        current_quantity:int = 0
        for _, row in self.df.iterrows():
            if self.check_if_category(row['Produto']):
                current_category = self.format_category(row['Produto'])
            else:
                if self.check_hifen_value_instead_numeric(row['Quantidade (L.)']):
                    current_quantity = 0
                else:
                    current_quantity = self.format_numeric_value(row['Quantidade (L.)'])
                data_list.append(self.make_new_entry_produto(current_category, self.format_category(row['Produto']), current_quantity, self.year))
        self.dict_producao_clean.update({"data_producao" : data_list})