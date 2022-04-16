import pandas as pd

data = pd.read_csv('food.csv')
new_data = ['Data.Carbohydrate', 'Data.Cholesterol', 'Data.Fiber', 'Data.Protein', 'Data.Fat.Monosaturated Fat', 
             'Data.Fat.Polysaturated Fat', 'Data.Fat.Saturated Fat', 'Data.Fat.Total Lipid', 'Data.Major Minerals.Iron',
             'Data.Major Minerals.Magnesium', 'Data.Major Minerals.Phosphorus', 'Data.Major Minerals.Potassium', 'Data.Major Minerals.Sodium',
             'Data.Major Minerals.Zinc', 'Data.Vitamins.Vitamin A - RAE', 'Data.Vitamins.Vitamin B12', 'Data.Vitamins.Vitamin B6',
             'Data.Vitamins.Vitamin C', 'Data.Vitamins.Vitamin E', 'Data.Vitamins.Vitamin K']

d = data.groupby('Category').mean()[new_data]
print(d)
pd.DataFrame(d).to_csv('final.csv')