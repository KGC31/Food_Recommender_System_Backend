from pydantic import BaseModel
from typing import Optional

class NutritionBaseModel(BaseModel):
    nutrition: str
    nutrition_class: str

class NutritionCreate(NutritionBaseModel):
    pass

class MacrosNutritionInfo(BaseModel):
    water_g:                    Optional[float] = None
    protein_g:                  Optional[float] = None
    fat_g:                      Optional[float] = None
    carbohydrate_g:             Optional[float] = None
    fiber_g:                    Optional[float] = None
    ash_g:                      Optional[float] = None
    
    def get_nutrition_class(self):
        return "macros_nutrition_info"
    
class SugarsNutritionInfo(BaseModel):
    total_sugar_g:              Optional[float] = None
    galactose_g:                Optional[float] = None
    maltose_g:                  Optional[float] = None
    lactose_g:                  Optional[float] = None
    fructose_g:                 Optional[float] = None
    glucose_g:                  Optional[float] = None
    sucrose_g:                  Optional[float] = None
    
    def get_nutrition_class(self):
        return "sugars_nutrition_info"
    
class MineralsNutritionInfo(BaseModel):
    calcium_mg:                 Optional[float] = None
    iron_mg:                    Optional[float] = None
    magnesium_mg:               Optional[float] = None
    manganese_mg:               Optional[float] = None
    phosphorus_mg:              Optional[float] = None
    potassium_mg:               Optional[float] = None
    sodium_mg:                  Optional[float] = None
    zinc_mg:                    Optional[float] = None
    copper_mcg:                 Optional[float] = None
    selenium_mcg:               Optional[float] = None
    
    def get_nutrition_class(self):
        return "minerals_nutrition_info"
    
class VitaminsNutritionInfo(BaseModel):
    vitamin_c_mg:               Optional[float] = None
    vitamin_b1_mg:              Optional[float] = None
    vitamin_b2_mg:              Optional[float] = None
    vitamin_pp_mg:              Optional[float] = None
    vitamin_b5_mg:              Optional[float] = None
    vitamin_b6_mg:              Optional[float] = None
    folate_mcg:                 Optional[float] = None
    vitamin_b9_mcg:             Optional[float] = None
    biotin_mcg:                 Optional[float] = None
    vitamin_b12_mcg:            Optional[float] = None
    vitamin_a_mcg:              Optional[float] = None
    vitamin_d_mcg:              Optional[float] = None
    vitamin_e_mg:	            Optional[float] = None
    vitamin_k_mcg:	            Optional[float] = None
    
    def get_nutrition_class(self):
        return "vitamins_nutrition_info"

class CarotenoidsNutritionInfo(BaseModel):
    beta_carotene_mcg:          Optional[float] = None
    alpha_carotene_mcg:         Optional[float] = None
    beta_cryptoxanthin_mcg:     Optional[float] = None
    lycopene_mg:                Optional[float] = None
    
    def get_nutrition_class(self):
        return "carotenoids_nutrition_info"
    
class PurinesNutritionInfo(BaseModel):
    purines_mg:                 Optional[float] = None
    
    def get_nutrition_class(self):
        return "purines_nutrition_info"
    
class IsoflavonesNutritionInfo(BaseModel):
    isoflavones_mg:             Optional[float] = None
    daidzein_mg:                Optional[float] = None
    genistein_mg:               Optional[float] = None
    glycitein_mg:               Optional[float] = None
    
    def get_nutrition_class(self):
        return "isoflavones_nutrition_info"
    
class LipidNutritionInfo(BaseModel):
    palmitic_c16_0:             Optional[float] = None
    margaric_c17_0:             Optional[float] = None
    stearic_c18_0:              Optional[float] = None
    arachidic_c20_0:            Optional[float] = None
    behenic_c22_0:              Optional[float] = None
    lignoceric_c24_0:           Optional[float] = None
    myristoleic_c14_1:          Optional[float] = None
    palmitoleic_c16_1:          Optional[float] = None
    oleic_c18_1:                Optional[float] = None
    linoleic_c18_2_n6:          Optional[float] = None
    linolenic_c18_3_n3:         Optional[float] = None
    arachidonic_c20_4:          Optional[float] = None
    epa_c20_5_n3:               Optional[float] = None
    dha_c22_6_n3:               Optional[float] = None
    cholesterol:                Optional[float] = None
    phytosterol:                Optional[float] = None
    total_saturated_fat:        Optional[float] = None
    total_monounsaturated_fat:  Optional[float] = None
    total_polyunsaturated_fat:  Optional[float] = None
    total_trans_fat:            Optional[float] = None
    
    def get_nutrition_class(self):
        return "lipid_nutrition_info"
    
class AminoAcidsNutritionInfo(BaseModel):
    lysine_mg:                  Optional[float] = None
    methionine_mg:              Optional[float] = None
    tryptophan_mg:              Optional[float] = None
    phenylalanine_mg:           Optional[float] = None
    threonine_mg:               Optional[float] = None
    valine_mg:                  Optional[float] = None
    leucine_mg:                 Optional[float] = None
    isoleucine_mg:              Optional[float] = None
    arginine_mg:                Optional[float] = None
    histidine_mg:               Optional[float] = None
    cystine_mg:                 Optional[float] = None
    tyrosine_mg:                Optional[float] = None
    alanine_mg:                 Optional[float] = None
    aspartic_acid_mg:           Optional[float] = None
    glutamic_acid_mg:           Optional[float] = None
    glycine_mg:                 Optional[float] = None
    proline_mg:                 Optional[float] = None
    serine_mg:                  Optional[float] = None
    
    def get_nutrition_class(self):
        return "amino_acids_nutrition_info"