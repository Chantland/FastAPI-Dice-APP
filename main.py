from typing import Union, Optional, List
from fastapi import FastAPI, Request, File, UploadFile, status, Form

from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid


import cv2
import numpy as np

app = FastAPI()


######## The following code was repurposed from https://www.youtube.com/watch?v=3vfum74ggHE&t=94s ######
import models
from database import SessionLocal, engine

# Dependency
def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()


####################

########### For Dice Picture ##########
import Dice_Picture

# pic = Dice_Picture.dicePic("static/images/J&E_Saint_L.jpg")
# pic = Dice_Picture.dicePic("Images_DELETE\\J&E_Abby_Wedding.jpg")
pic = Dice_Picture.dicePic("static/images/J&E_Saint_L.jpg", inp_prompt=False)
pic.possible_blocks()   

#######################################


app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/templates/images", StaticFiles(directory="templates/images"), name="images")

templates = Jinja2Templates(directory="templates")



@app.get("/")    
async def main(request: Request):
	return templates.TemplateResponse("main.html",{"request":request})  #for localizing to a page





@app.post("/uploadfiles/")
async def create_upload_file(request: Request, file: UploadFile):
    response = f'images/{file.filename}'
    return templates.TemplateResponse("item.html",{"request":request, "bef_img": response})




@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


# @app.post("/uploadfiles/")
# async def create_upload_file(request: Request, file: UploadFile = File(...)):
#     bin_data = file.read()
#     return FileResponse(bin_data)


# @app.post("/uploadfiles/")
# async def create_upload_file(request: Request, file: UploadFile = File(...)):
#     bin_data = file.file.read()
#     return {"message":bin_data}

# @app.post("/uploadfiles/")
# async def create_upload_file(request: Request, file: Union[bytes, None] = File(default=None)):
#     return FileResponse(file)

# @app.post("/uploadfiles/")
# async def create_upload_file(request: Request, file: UploadFile):
#     response = FileResponse(f'static/images/{file.filename}')
#     return templates.TemplateResponse("item.html",{"request":request, "bef_img": response})



#probably delete this in time
@app.get("/items/{ids}", response_class=HTMLResponse)
async def read_item(request: Request, ids: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": ids})



