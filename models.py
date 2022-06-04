from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship

from database import Base


# Tables (consider deleting whatever as needed)
class Pics(Base):
    __tablename__ = "pics"

    id = Column(Integer, primary_key=True, index=True)
    Bef_filename = Column(String)
    Aft_filename = Column(String)
    Computed = Column(Boolean, default=False)
    
    size_x = Column(Integer)
    size_y = Column(Integer)
    data = Column(Unicode)

    potent_dice_dim = relationship("Dice_Dim", cascade="all,delete-orphan", back_populates="original_img")

class Dice_Dim(Base):
    __tablename__ = "dice_dim"
    id = Column(Integer, primary_key=True, index=True)
    size_x = Column(Integer)
    size_y = Column(Integer)
    orig_id = Column(Integer, ForeignKey("pics.id"))

    original_img = relationship("Pics", back_populates="potent_dice_dim")