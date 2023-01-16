from fastapi import FastAPI, Form, HTTPException, status, Depends
from pydantic import BaseModel
import traceback
from util import *
from loger import *
import os
import secrets

API_KEY = os.getenv("API_KEY")

# Declaring our FastAPI instance
app = FastAPI()

## Auth function
def auth_key(api_key:str):
    if secrets.compare_digest(api_key, API_KEY):
        # Allow if key matched
        pass
    else:
        # Raise Exception if not 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )

class Transaction(BaseModel):
    msg: str

@app.post("/class", dependencies=[Depends(auth_key)], status_code=status.HTTP_201_CREATED)
def categorize(input: Transaction):
    text = input.msg
    output = {}
    if text =='':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty message"
        )
    try:
        infoLogger.info(f"Received following message: {text}")
        infoLogger.info("Processing..")
        matched, all_fields =  match_transaction(text)
        infoLogger.info("Done!")
        if matched is None:
            infoLogger.info("Error logged.")
            msg = 'API Error logged. Contact maintainer'
        elif matched == True:
            msg = 'matched'
        elif matched ==False:
            msg = 'not matched'
        output['fields']= all_fields
        output['msg'] = msg
        return output
    except Exception as e:
        errorLogger.exception(e, exc_info=True)
        errorLogger.error("API Error logged.")
        infoLogger.error("API Error logged.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="API Error logged. Contact maintainer")
