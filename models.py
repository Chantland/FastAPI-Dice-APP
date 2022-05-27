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

    # converted_img = relationship("Aft_img", cascade="all,delete-orphan", back_populates="original_img")

# class Aft_img(Base):
#     __tablename__ = "after_image"
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String)
#     size_x = Column(Integer)
#     size_y = Column(Integer)
#     orig_id = Column(Integer, ForeignKey("before_image.id"))

#     original_img = relationship("Bef_img", back_populates="converted_img")