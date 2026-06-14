import uuid
from uuid6 import uuid7
from sqlalchemy import func, types
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.postgres.database import Base, engine

class FoodMetaData(Base):
    __tablename__ = "food_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )
    name_vi = Column(String, unique=True, index=True)
    name_en = Column(String, unique=True, index=True)
    kcal_per_100g = Column(Float)
    kj_per_100g = Column(Float)
    source = Column(String, default="")
    source_url = Column(String, default="")
    food_category_id = Column(types.Uuid, ForeignKey("food_category.id"))
    
class NutritionMetaData(Base):
    __tablename__ = "nutrition_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )
    nutrition = Column(String, unique=True, index=True)
    nutrition_class = Column(String, index=True)
    
class FoodNutrients100g(Base):
    __tablename__ = "food_nutrients_100g"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7
    )
    food_id = Column(types.Uuid, ForeignKey("food_metadata.id"))
    nutrition_id = Column(types.Uuid, ForeignKey("nutrition_metadata.id"))
    value = Column(Float)

class FoodCategory(Base):
    __tablename__ = "food_category"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )
    category_name_vi = Column(String, unique=True, index=True)
    category_name_en = Column(String, unique=True, index=True)