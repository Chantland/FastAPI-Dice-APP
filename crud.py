from sqlalchemy.orm import Session

from typing import Union

import models



def pic_inject(db: Session, pic_fail: Union[str, None] = None):
    pic_list = db.query(models.Pics).all()
    return {"pic_fail": pic_fail, "pic_list":pic_list}


