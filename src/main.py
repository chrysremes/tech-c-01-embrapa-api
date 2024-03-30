from enum import Enum
import uvicorn
from fastapi import FastAPI, responses
from EmbrapaURL import EmbrapaURL

class DataTypeReturn(str, Enum):
    url = "url"
    df_str = "df_str"
    df_csv = "df_csv"
    df_dict = "df_dict"
    df_json = "df_json"
    df_html_tab = "df_html_tab"

app = FastAPI()

@app.get('/')
def root():
    return {"main":"page"}

@app.get('/get_url/')
def read_data(option_id:str, suboption_id:str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return {"url" : embrapa.url_request}

@app.get('/get_df_as_str/')
def read_data(option_id:str, suboption_id:str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return {"df" : embrapa.df.to_string()}

@app.get('/get_df_as_csv/')
def read_data(option_id:str, suboption_id:str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return {"df" : embrapa.df.to_csv()}

@app.get('/get_df_as_dict/')
def read_data(option_id:str, suboption_id:str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return {"df" : embrapa.df.to_dict()}

@app.get('/get_df_as_json/')
def read_data(option_id:str, suboption_id:str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return {"df" : embrapa.df.to_json()}

@app.get('/get_df_as_html_table/')
def read_data(option_id:str, suboption_id:str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return responses.HTMLResponse(content=embrapa.df.to_html(), status_code=200)

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)



