from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    product = relationship("Product", back_populates="images")
