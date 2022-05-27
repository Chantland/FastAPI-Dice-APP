from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship

from database import Base

# old database, removed the 2nd table because it appears not necessary
# Tables (consider deleting whatever as needed)
class Bef_img(Base):
    __tablename__ = "before_image"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    size_x = Column(Integer)
    size_y = Column(Integer)
    data = Column(Unicode)

    converted_img = relationship("Aft_img", cascade="all,delete-orphan", back_populates="original_img")

class Aft_img(Base):
    __tablename__ = "after_image"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    size_x = Column(Integer)
    size_y = Column(Integer)
    orig_id = Column(Integer, ForeignKey("before_image.id"))

    original_img = relationship("Bef_img", back_populates="converted_img")