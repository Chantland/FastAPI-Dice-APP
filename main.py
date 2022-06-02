# requirements file: pip install -r requirements.txt
# does not include: fastapi Uvicorn, SQLalchemy, CV2, or multipart 
# (pip install fastapi uvicorn SQLalchemy opencv-python python-multipart)

from typing import Union, Optional, List
from fastapi import Depends, FastAPI, Request, File, UploadFile, status, Form

from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

import uuid

import cv2
import numpy as np

import models
from database import SessionLocal, engine



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/templates/images", StaticFiles(directory="templates/images"), name="images")

templates = Jinja2Templates(directory="templates")

# run on command
import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



# Dependency
def get_db():
    db = SessionLocal()    
    try:
        yield db
    finally:
        db.close()


####### demo dependancies ########

# from pydantic import BaseSettings


# class Settings(BaseSettings):
#     work_dir: str = 'static/upload/'
#     thumb_width: int = 340
#     thumb_height: int = 800
#     thumb_size: tuple = (300, 500)
#     max_imgWidth: int = 600
#     max_imgHeight: int = 800


# settings = Settings()



# import os.path
# import uuid
# from pathlib import Path
# def create_workspace():
#     """
#     Return workspace 
#     """
#     # base directory
#     work_dir = Path(settings.work_dir)
#     # UUID to prevent file overwrite
#     request_id = Path(str(uuid.uuid4())[:8])
#     # path concat instead of work_dir + '/' + request_id
#     workspace = work_dir / request_id
#     if not os.path.exists(workspace):
#         # recursively create workdir/unique_id
#         os.makedirs(workspace)

#     return workspace
#####

########### For Dice Picture ##########


import Dice_Picture

# # pic = Dice_Picture.dicePic("static/images/J&E_Saint_L.jpg")
# # pic = Dice_Picture.dicePic("Images_DELETE\\J&E_Abby_Wedding.jpg")
# pic = Dice_Picture.dicePic("static/images/J&E_Saint_L.jpg", inp_prompt=False)  
# pic.possible_blocks()                       
# pic.dice_alt(pic.posDiceNum[7])             
# pic.inp_Dice(perc_pip=.06, dice_dict=None)                                            
# pic.showIm(pic.img_Dice_Pic, print_img=False)   
# pic.printIm()


#######################################
# class ItemCreate(ItemBase):
#     pass

# def create_user_item(db: Session, item: ItemCreate, user_id: int):
#     db_item = models.Aft_img(owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


@app.get("/")    
async def main(request: Request, db: Session = Depends(get_db)):
    Bef_img = db.query(models.Pics).all()
    return templates.TemplateResponse("main.html",{"request":request, "pic_list":Bef_img})  #for localizing to a page


@app.post("/originaluploadfiles/")
async def create_upload_file(request: Request, file: UploadFile):
    response = f'images/{file.filename}'
    return templates.TemplateResponse("item.html",{"request":request, "bef_img": response})

# # working 1
# @app.post("/uploadfiles/")
# async def create_upload_file(request: Request, file: UploadFile, db: Session = Depends(get_db)):
#     url = app.url_path_for("main")
#     new_img = models.Pics(filename = file.filename)
#     db.add(new_img)
#     db.commit()
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
# <!-- <img src="/uploadfiles/" alt="Wedding outfit before dice" title="After"/> --> <!-- for working draft 1 -->

# # # working 2
# @app.post("/uploadfiles/")
# async def create_upload_file(request: Request, file: UploadFile, db: Session = Depends(get_db)):
#     url = app.url_path_for("main")

#     contents = await file.read()
#     nparr = np.fromstring(contents, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     size_x, size_y = img.shape[0:2]
#     #img_show(img) #may not be necessary but proof of concept,
#     cv2.imwrite("./static/images/placeholder.png", img)

#     new_img = models.Pics(filename = file.filename, size_x = size_x, size_y=size_y, data=img)
#     db.add(new_img)
#     db.commit()
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
# # # <!-- <img class= "optional_show" src="{{ url_for('static', path='images/placeholder.png') }}" alt="before" title="before" onerror="imgError(this);"/> --> 


import Dice_Picture

# # pic = Dice_Picture.dicePic("static/images/J&E_Saint_L.jpg")
# # pic = Dice_Picture.dicePic("Images_DELETE\\J&E_Abby_Wedding.jpg")
# pic = Dice_Picture.dicePic("static/images/J&E_Saint_L.jpg", inp_prompt=False)                  
# pic.dice_alt(pic.posDiceNum[7])             
# pic.inp_Dice(perc_pip=.06, dice_dict=None)                                            
# pic.showIm(pic.img_Dice_Pic, print_img=False)   
# pic.printIm()






# working 3

@app.post("/uploadfiles/")
async def create_upload_file(request: Request, file: UploadFile, db: Session = Depends(get_db)):
    url = app.url_path_for("main")

    try:
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)   #I wonder if the dice_pic could do this... best check later
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        size_x, size_y = img.shape[0:2]
        file_path = "./static/images/" + file.filename
    except:
        pic_fail = True
        Bef_img = db.query(models.Pics).all()
        return templates.TemplateResponse("main.html", {"request": request, "pic_fail": pic_fail, "pic_list":Bef_img})

    cv2.imwrite(file_path, img)

    try:
        pic = Dice_Picture.dicePic(file_path, inp_prompt=False)
    except:
        sassy = True
        Bef_img = db.query(models.Pics).all()
        return templates.TemplateResponse("main.html", {"request": request, "sassy": sassy, "pic_list":Bef_img})

    Dice_option_list = pic.posDiceNum

    before_img = models.Pics(Bef_filename = file.filename, size_x = size_x, size_y=size_y, data=img)
    db.add(before_img)
    db.commit()
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


    

@app.get("/delete/{pic_id}")
def delete(request: Request, pic_id: int, db: Session = Depends(get_db)):
    pic_d = db.query(models.Pics).filter(models.Pics.id == pic_id).first()
    db.delete(pic_d)
    db.commit()

    url = app.url_path_for("main")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    



@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

