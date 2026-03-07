import uuid
from sqlalchemy import func, types
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID

from src.db.database import Base, engine

class DietTag(Base):
    __tablename__ = "diet_tags"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    name = Column(String, unique=True, index=True)
    
class FoodDietTag(Base):
    __tablename__ = "food_diet_tags"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    food_id = Column(types.Uuid, ForeignKey("food_metadata.id"))
    diet_tag_id = Column(types.Uuid, ForeignKey("diet_tags.id"))
    
class CuisineTag(Base):
    __tablename__ = "cuisine_tags"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    name = Column(String, unique=True, index=True)
    
class FoodCuisineTag(Base):
    __tablename__ = "food_cuisine_tags"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    food_id = Column(types.Uuid, ForeignKey("food_metadata.id"))
    cuisine_tag_id = Column(types.Uuid, ForeignKey("cuisine_tags.id"))

class FoodMetaData(Base):
    __tablename__ = "food_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    name = Column(String, unique=True, index=True)
    alternate_names = Column(String)
    description = Column(String)
    ingredients = Column(JSONB)
    
class NutritionMetaData(Base):
    __tablename__ = "nutrition_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    nutrition = Column(String, unique=True, index=True)
    
class FoodNutrients(Base):
    __tablename__ = "food_nutrients"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    food_id = Column(types.Uuid, ForeignKey("food_metadata.id"))
    nutrition_id = Column(types.Uuid, ForeignKey("nutrition_metadata.id"))
    value = Column(Float)