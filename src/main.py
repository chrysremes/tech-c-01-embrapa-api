from typing import Annotated
from auth import post_token
from auth.Auth import User, get_current_active_user

import uvicorn
from fastapi import FastAPI, Path, Depends

from EmbrapaTreatData import EmbrapaData
from EmbrapaWebScrap import EmbrapaWebScrap
from EmbrapaDefs import DataOption, DataSubOption, EmbrapaPages

###########################################
#  Required Imports above
###########################################

# Instantiate the API
app = FastAPI()

# Include the route for JWT Authentication
app.include_router(post_token.router)


###########################################
#  API Paths in the following
###########################################

# Root

@app.get('/', tags=["Welcome - Root"])
def root():
    return {"root":"page"}

# Embrapa Raw: read_raw_dict

@app.get('/read_raw_dict/year={year}/option={option_id}/suboption={suboption_id}', tags=["Embrapa Raw"])
def read_raw_data_dict(
        year: Annotated[int, Path(title="The ID of the item to get", ge=EmbrapaPages.START_YEAR, le=EmbrapaPages.LAST_YEAR)], 
        option_id: DataOption, 
        suboption_id: DataSubOption,
        current_user: Annotated[User, Depends(get_current_active_user)]
    )->dict:
    """
    'read_raw_dict' API path receives the year, option and suboption, 
    and returns a raw dictionary (json-like format) with data Scraped 
    from the Embrapa Website.
    Also, this API path requires JWT authentication 
    (implied by the use of argument "current_user: Annotated[User, Depends(get_current_active_user)]").
    Notice that when requesting data from a option without suboption, 
    then it should be used 'suboption=None'.
    
    Request example:
    ./read_raw_dict/year=2022/option=producao/suboption=None
    """

    if suboption_id is DataSubOption.StrNone:
        suboption_id=None
    
    embrapa = EmbrapaWebScrap(year=year, option=option_id, suboption=suboption_id)
    embrapa.request_and_save_to_df()

    return {"df-dict" : embrapa.df.to_dict()}



# Embrapa Clean: read_clean_data

@app.get('/read_clean_data/year={year}/option={option_id}/suboption={suboption_id}', tags=["Embrapa Clean"])
def read_clean_data(
        year: Annotated[int, Path(title="The ID of the item to get", ge=EmbrapaPages.START_YEAR, le=EmbrapaPages.LAST_YEAR)], 
        option_id: DataOption, 
        suboption_id: DataSubOption
    )->dict:
    """
    'read_clean_data' API path receives the year, option and suboption, 
    and returns a full dictionary (json-like format) with data Scraped 
    and properly cleaned/formated from the Embrapa Website.
    This API path does not require JWT authentication.
    Notice that when requesting data from a option without suboption, 
    then it should be used 'suboption=None'.
    
    Request example:
    ./read_clean_data/year=2022/option=producao/suboption=None
    """
    
    if suboption_id is DataSubOption.StrNone:
        suboption_id=None
    
    embrapa_scrap = EmbrapaWebScrap(year=year, option=option_id, suboption=suboption_id)
    embrapa_scrap.request_and_save_to_df()

    embrapa_data = EmbrapaData(embrapa_scrap.df, year=year, option=option_id, suboption=suboption_id)
    cleaned_dict = embrapa_data.get_cleaned_data_dict()

    return cleaned_dict


###########################################
#  Uvicorn API Run below
###########################################

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)