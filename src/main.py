from datetime import timedelta
from typing import Annotated, Any

import json

import uvicorn
from fastapi import FastAPI, HTTPException, responses, status, Depends

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from pydantic import BaseModel
from enum import Enum

from EmbrapaWebScrap import EmbrapaWebScrap

from auth import Token, User, authenticate_user, create_access_token, get_current_active_user, read_users_db

ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

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
    return {"root":"page"}

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(read_users_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get('/items/')
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token" : token}

@app.get('/get/return_type={return_type}/year={year}/option={option_id}')
def read_data(return_type: DataTypeReturn, year: int, option_id: str, suboption_id: str | None = None):
    embrapa = EmbrapaWebScrap(year=year, option=option_id,suboption=suboption_id)
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



