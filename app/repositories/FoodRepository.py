from sqlalchemy import select
import logging

from app.db.postgres.schema import FoodCategory, FoodMetaData

class FoodRepository:
    def __init__(self, db):
        self.db = db
        
    def create(self, data: FoodMetaData) -> FoodMetaData:
        food = FoodMetaData(
            name_vi=data.name_vi,
            name_en=data.name_en,
            kcal_per_100g=data.kcal_per_100g,
            kj_per_100g=data.kj_per_100g,
            source=data.source,
            source_url=data.source_url,
            food_category_id=data.food_category_id
        )
        
        self.db.add(food)
        self.db.flush()
        
        return food
        
    def get_foods_by_kcal_range(self, min_kcal: float, max_kcal: float) -> list[FoodMetaData]:     
        try:
            query = select(
                    FoodMetaData.id,
                    FoodMetaData.name_vi,
                    FoodMetaData.name_en,
                    FoodMetaData.kcal_per_100g,
                    FoodMetaData.kj_per_100g,
                    FoodMetaData.source,
                    FoodMetaData.source_url
                )\
                .filter(
                    FoodMetaData.kcal_per_100g >= min_kcal,
                    FoodMetaData.kcal_per_100g <= max_kcal
                )
                
            result = self.db.execute(query).mappings().all()
            
            return result
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            raise e
        
    def get_or_create_category(self, category_name_vi: str, category_name_en: str):
        try:
            query = select(FoodCategory).filter(
                FoodCategory.category_name_vi == category_name_vi,
                FoodCategory.category_name_en == category_name_en
            )
            category = self.db.execute(query).scalar_one_or_none()
            
            if category:
                return category
            
            new_category = FoodCategory(
                category_name_vi=category_name_vi,
                category_name_en=category_name_en
            )
            self.db.add(new_category)
            self.db.flush()
            
            return new_category
        
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            raise e