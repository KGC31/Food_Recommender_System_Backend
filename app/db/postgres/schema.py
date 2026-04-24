import uuid
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
        server_default=func.gen_random_uuid()
    )
    name_vi = Column(String, unique=True, index=True)
    name_en = Column(String, unique=True, index=True)
    kcal_per_100g = Column(Float)
    kj_per_100g = Column(Float)
    
class NutritionMetaData(Base):
    __tablename__ = "nutrition_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    nutrition = Column(String, unique=True, index=True)
    nutrition_class = Column(String, index=True)
    
class FoodNutrients100g(Base):
    __tablename__ = "food_nutrients_100g"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    food_id = Column(types.Uuid, ForeignKey("food_metadata.id"))
    nutrition_id = Column(types.Uuid, ForeignKey("nutrition_metadata.id"))
    value = Column(Float)
    
class CountryMetaData(Base):
    __tablename__ = "country_metadata"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    name = Column(String, unique=True, index=True)
    
class FoodCountry(Base):
    __tablename__ = "food_country"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    food_id = Column(types.Uuid, ForeignKey("food_metadata.id"))
    country_id = Column(types.Uuid, ForeignKey("country_metadata.id"))