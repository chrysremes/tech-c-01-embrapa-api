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

@app.get('/get/return_type={return_type}/option={option_id}')
def read_data(return_type: DataTypeReturn, option_id: str, suboption_id: str | None = None):
    embrapa = EmbrapaURL(option=option_id,suboption=suboption_id)
    embrapa.request_and_save_to_df()
    if return_type is DataTypeReturn.url:
        return {"url" : embrapa.url_request}
    elif return_type is DataTypeReturn.df_str:
        return {"df-str" : embrapa.df.to_string()}
    elif return_type is DataTypeReturn.df_csv:
        return {"df-csv" : embrapa.df.to_csv()}
    elif return_type is DataTypeReturn.df_dict:
        return {"df-dict" : embrapa.df.to_dict()}
    elif return_type is DataTypeReturn.df_json:
        return {"df-json" : embrapa.df.to_json()}
    elif return_type is DataTypeReturn.df_html_tab:
        return responses.HTMLResponse(content=embrapa.df.to_html(), status_code=200)
    else:
        enums = [enum0.value for enum0 in DataTypeReturn]
        return {"error": "Incorrect Return Type. Choose an option from {enums}"}

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)



