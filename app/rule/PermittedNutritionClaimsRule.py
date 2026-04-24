from typing import List

from app.utils.enums import PermittedNutritionClaimsEnum
from app.utils.types import FoodNutritionalInfo

class PermittedNutritionClaimsRule:
    def __init__(self):
        self.rules = {
            # ENERGY
            PermittedNutritionClaimsEnum.LOW_ENERGY: lambda f: f.energy_kcal <= 40,
            PermittedNutritionClaimsEnum.ENERGY_FREE: lambda f: f.energy_kcal <= 4,

            # FAT
            PermittedNutritionClaimsEnum.LOW_FAT: lambda f: f.macros_fat_g <= 3,
            PermittedNutritionClaimsEnum.FAT_FREE: lambda f: f.macros_fat_g <= 0.5,

            # SAT FAT
            PermittedNutritionClaimsEnum.LOW_SATURATED_FAT: lambda f: f.lipids_total_saturated_fat_g <= 1.5 if getattr(f, "lipids_total_saturated_fat_g") else False,
            PermittedNutritionClaimsEnum.SATURATED_FAT_FREE: lambda f: f.lipids_total_saturated_fat_g <= 0.1 if getattr(f, "lipids_total_saturated_fat_g") else False,

            # SUGARS
            PermittedNutritionClaimsEnum.LOW_SUGARS: lambda f: f.sugars_total_sugar_g <= 5,
            PermittedNutritionClaimsEnum.SUGARS_FREE: lambda f: f.sugars_total_sugar_g <= 0.5,

            # SODIUM
            PermittedNutritionClaimsEnum.LOW_SODIUM: lambda f: f.minerals_sodium_mg <= 120,
            PermittedNutritionClaimsEnum.VERY_LOW_SODIUM: lambda f: f.minerals_sodium_mg <= 40,
            PermittedNutritionClaimsEnum.SODIUM_FREE: lambda f: f.minerals_sodium_mg <= 5,

            # FIBRE
            PermittedNutritionClaimsEnum.SOURCE_OF_FIBRE: lambda f: f.macros_fiber_g >= 3,
            PermittedNutritionClaimsEnum.HIGH_FIBRE: lambda f: f.macros_fiber_g >= 6,

            # PROTEIN (derived)
            PermittedNutritionClaimsEnum.SOURCE_OF_PROTEIN: self._is_source_of_protein,
            PermittedNutritionClaimsEnum.HIGH_PROTEIN: self._is_high_protein,

            # OMEGA 3 (derived)
            PermittedNutritionClaimsEnum.SOURCE_OF_OMEGA_3_FATTY_ACIDS: self._has_omega3,
        }
        
    def _protein_energy_percent(self, f: FoodNutritionalInfo) -> float:
        if f.energy_kcal == 0:
            return 0
        return (f.macros_protein_g * 4 / f.energy_kcal) * 100

    def _is_source_of_protein(self, f: FoodNutritionalInfo) -> bool:
        return self._protein_energy_percent(f) >= 12

    def _is_high_protein(self, f: FoodNutritionalInfo) -> bool:
        return self._protein_energy_percent(f) >= 20

    def _has_omega3(self, f: FoodNutritionalInfo) -> bool:
        omega3 = (
            getattr(f, "lipids_fatty_acids_epa_c20_5_n3_g", 0) +
            getattr(f, "lipids_fatty_acids_dha_c22_6_n3_g", 0) +
            getattr(f, "lipids_fatty_acids_linolenic_c18_3_n3_g", 0)
        )
        return omega3 >= 0.3
    
    def classify(self, food: FoodNutritionalInfo) -> List[PermittedNutritionClaimsEnum]:
        tags = []

        for claim, rule in self.rules.items():
            try:
                if rule(food):
                    tags.append(claim)
            except Exception:
                continue

        return tags