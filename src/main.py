from datetime import timedelta
from typing import Annotated, Any

import uvicorn
from fastapi import FastAPI, Path, HTTPException, responses, status, Depends

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from EmbrapaWebScrap import EmbrapaWebScrap
from EmbrapaDefs import DataOption, DataSubOption, DataTypeReturn

from auth import Token, User, authenticate_user, create_access_token, read_users_db

ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

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

@app.get('/get/return_type={return_type}/year={year}/option={option_id}/suboption={suboption_id}')
def read_data(
    return_type: DataTypeReturn, 
    year: Annotated[int, Path(title="The ID of the item to get", ge=1970, le=2022)], 
    option_id: DataOption, 
    suboption_id: DataSubOption,
    # current_user: Annotated[User, Depends(get_current_active_user)]
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

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)



