from flask import Flask, redirect, url_for, render_template
import requests
import os
import math 
from flask import request
import pandas as pd
from flask import Flask, redirect, url_for, render_template, request, session, flash
from get_recommendations import get_recomm_df
from get_restrictions import recommendation

app = Flask(__name__)
app.config['SECRET_KEY'] = "priyamane"

food_item_selected = ""
lifestyle_selected = ""
disease_to_avoid_selected = ""

@app.route('/', methods=['GET', 'POST'])
def get_user_details():
    lifestyle = ["Athletic Lifestyle","Active & Healthy","Inactive but healthy choices","Inactive & unhealthy"]
    diseases_to_avoid = ["Diabetes", "Heart Disease", "Obesity", "Skin Problems", "Liver Damage","Blood Pressure"]
    return render_template('user_details.html', data={"lifestyle":lifestyle, "diseases_to_avoid":diseases_to_avoid})

@app.route('/get_food_item', methods=['GET', 'POST'])
def get_food_item():
    global lifestyle_selected
    global disease_to_avoid_selected
    food_items = pd.read_csv('clustered_data.csv')['Category']
    lifestyle_selected = request.form["lifestyle"]
    disease_to_avoid_selected = request.form["disease_to_avoid"]
    return render_template('index.html', data={"food_items":food_items})

@app.route('/get_recommendations', methods=['GET','POST'])
def get_recommendations():
    global food_item_selected
    food_item_selected = request.form["food_item"]

    imp_f = ['nutrient_total_fat', 'nutrient_total_carb', 'nutrient_protein',
        'nutrient_sat_fat', 'nutrient_cholesterol', 'nutrient_sodium', 'nutrient_fiber',
        'nutrient_calcium', 'nutrient_vitamin_a']

    df_ans = get_recomm_df(lifestyle_selected, food_item_selected).reset_index()

    for f in imp_f:
        df_ans[f] = df_ans[f].apply(lambda x: math.ceil(x*100)/100)

    _, _, _, restrictions = recommendation(food_item_selected,disease_to_avoid_selected)

    images = ["static/nutcase_vegan.jpeg","static/sardines.jpeg","static/radi.jpeg","static/moz.jpeg","static/upma.jpeg"]

    return render_template('results_page.html', data={"food_i_selected":food_item_selected, 
                                                        "lifestyle_selected":lifestyle_selected,
                                                        "disease_to_avoid" : disease_to_avoid_selected,
                                                        "df_ans" : df_ans,
                                                        "restrictions":restrictions,
                                                        "images":images
                                                        })

if __name__ == '__main__':
    app.run(debug=True)
