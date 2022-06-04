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

import models, crud, Dice_Picture
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







@app.get("/")    
async def main(request: Request, db: Session = Depends(get_db)):
    # Bef_img = db.query(models.Pics).all()
    # return templates.TemplateResponse("main.html",{"request":request, "pic_list":Bef_img})  #for localizing to a page
    return templates.TemplateResponse("main.html", {"request":request, **crud.pic_inject(db=db)})



# working 3
@app.post("/uploadfiles/")
async def create_upload_file(request: Request, file: UploadFile, db: Session = Depends(get_db)):
    url = app.url_path_for("main")

    # implement and scan the imgage (if no image or bad file submitted, send warning variable)
    # right now storing the size and data is superfluous, change later
    try:
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)   #I wonder if the dice_pic could do this... best check later
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        size_x, size_y = img.shape[0:2]
        file_path = "./static/images/" + file.filename
    except:
        pic_fail = "WARNING cannot read, make sure you are submitting a picture"
        return templates.TemplateResponse("main.html", {"request":request, **crud.pic_inject(pic_fail=pic_fail, db=db)})

    cv2.imwrite(file_path, img)

    # initiate dice image, if the image cannot be subdivided, send warning variable)
    try:
        pic = Dice_Picture.dicePic(file_path, inp_prompt=False)
    except:
        pic_fail = "WARNING The picture you chose cannot be evenly subdivided. Either crop it or choose a different picture"
        return templates.TemplateResponse("main.html", {"request":request, **crud.pic_inject(pic_fail=pic_fail, db=db)})
    
    before_img = models.Pics(Bef_filename = file.filename, size_x = size_x, size_y=size_y, data=img)
    db.add(before_img)
    db.commit()

    # add all the dice permutations (need to convert numpy integers to integers or else returns a blob)
    Dice_option_list = pic.posDiceNum
    dice_dimensions = []
    for YandX in Dice_option_list:
        model_input = models.Dice_Dim(size_x = int(YandX[1]), size_y = int(YandX[0]), orig_id = before_img.id)
        dice_dimensions.append(model_input)
    db.add_all(dice_dimensions)
    db.commit()

    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


    

@app.get("/delete/{pic_id}")
def delete(request: Request, pic_id: int, db: Session = Depends(get_db)):
    pic_d = db.query(models.Pics).filter(models.Pics.id == pic_id).first()
    db.delete(pic_d)
    db.commit()

    url = app.url_path_for("main")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    


@app.get("/dice_prog/")
def dice_prog(request: Request, dice_perm: int, db: Session = Depends(get_db)):
    print(dice_perm) #DELETE for checking number returned

    # find the original dice dimensions selected and the original file name.
    dice_dim_size = db.query(models.Dice_Dim).filter(models.Dice_Dim.id == dice_perm).first()
    orig_image = db.query(models.Pics).filter(models.Pics.id == dice_dim_size.orig_id).first()
    pic = Dice_Picture.dicePic("static/images/" + orig_image.Bef_filename, inp_prompt=False)
    dim_array = np.array([dice_dim_size.size_y, dice_dim_size.size_x])
    pic.dice_alt(dim_array)
    pic.inp_Dice(perc_pip=.06, dice_dict=None) 
    pic.printIm()

    orig_image.Aft_filename = pic.filename
    orig_image.Computed = True
    db.commit()


    Bef_img = db.query(models.Pics).all()
    return templates.TemplateResponse("main.html", {"request":request, **crud.pic_inject(db=db)})

    #working dice_prog1
# @app.get("/dice_prog/")
# def dice_prog(request: Request, dice_perm: Union[str, None] = None, db: Session = Depends(get_db)):
#     print(dice_perm)
#     pic_fail = True
#     Bef_img = db.query(models.Pics).all()
#     return templates.TemplateResponse("main.html", {"request": request, "pic_fail": pic_fail, "pic_list":Bef_img})
