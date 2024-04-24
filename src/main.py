from typing import Annotated
from auth import post_token
from auth.Auth import User, get_current_active_user

import uvicorn
from fastapi import FastAPI, Path, responses, Depends

from EmbrapaTreatData import EmbrapaData
from EmbrapaWebScrap import EmbrapaWebScrap
from EmbrapaDefs import DataOption, DataSubOption, DataTypeReturn, EmbrapaPages

app = FastAPI()
app.include_router(post_token.router)

@app.get('/', tags=["Welcome - Root"])
def root():
    return {"root":"page"}

@app.get('/read_raw_dict/year={year}/option={option_id}/suboption={suboption_id}', tags=["Embrapa Raw"])
def read_raw_data_dict(
        year: Annotated[int, Path(title="The ID of the item to get", ge=EmbrapaPages.START_YEAR, le=EmbrapaPages.LAST_YEAR)], 
        option_id: DataOption, 
        suboption_id: DataSubOption,
        # current_user: Annotated[User, Depends(get_current_active_user)]
    )->dict:
    if suboption_id is DataSubOption.StrNone:
        suboption_id=None
    embrapa = EmbrapaWebScrap(year=year, option=option_id, suboption=suboption_id)
    embrapa.request_and_save_to_df()
    return {"df-dict" : embrapa.df.to_dict()}

@app.get('/read_raw_any/return_type={return_type}/year={year}/option={option_id}/suboption={suboption_id}', tags=["Embrapa Raw"])
def read_raw_data_protected(
        return_type: DataTypeReturn, 
        year: Annotated[int, Path(title="The ID of the item to get", ge=EmbrapaPages.START_YEAR, le=EmbrapaPages.LAST_YEAR)], 
        option_id: DataOption, 
        suboption_id: DataSubOption,
        current_user: Annotated[User, Depends(get_current_active_user)]
    )->dict:
    if suboption_id is DataSubOption.StrNone:
        suboption_id=None
    embrapa = EmbrapaWebScrap(year=year, option=option_id, suboption=suboption_id)
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


@app.get('/read_clean_data/year={year}/option={option_id}/suboption={suboption_id}', tags=["Embrapa Clean"])
def read_clean_data(
        year: Annotated[int, Path(title="The ID of the item to get", ge=EmbrapaPages.START_YEAR, le=EmbrapaPages.LAST_YEAR)], 
        option_id: DataOption, 
        suboption_id: DataSubOption,
        # current_user: Annotated[User, Depends(get_current_active_user)]
    )->dict:
    
    if suboption_id is DataSubOption.StrNone:
        suboption_id=None
    
    embrapa_scrap = EmbrapaWebScrap(year=year, option=option_id, suboption=suboption_id)
    embrapa_scrap.request_and_save_to_df()

    embrapa_data = EmbrapaData(embrapa_scrap.df, year=year, option=option_id, suboption=suboption_id)
    cleaned_dict = embrapa_data.get_cleaned_data_dict()
    print(cleaned_dict)

    return cleaned_dict


if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)