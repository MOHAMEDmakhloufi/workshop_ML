from flask import Flask
from flask import render_template, request,  url_for

app = Flask(__name__)

def predict(curb_weight):
    import joblib
    import pandas as pd

    url_model=url_for('static', filename='price_car_prediction.pkl').strip('/')

    model = joblib.load(url_model)
    dataframe = pd.DataFrame({'curb-weight': [curb_weight]})
    resulta = model.predict(dataframe)
    return resulta[0]

@app.route('/', methods=('GET', 'POST'))
def baseTemplate():
    if request.method=='POST':
        weight = float(request.form['curb-weight'])
        price = float(request.form['price'])
        predict_price= predict(weight)
        if price > predict_price:
            msg= "Le prix affiché sur l'annonce est élevé car pour une voiture avec ce poids à vide, notre modèle prédit un prix égale à "+str(round(predict_price))+" $"
            return render_template('base.html', color="red", msg=msg, weight= weight, price=price)

        msg= "Vous allez faire une bonne affaire car pour une voiture avec ce poids à vide, notre modèle prédit un prix égale à "+str(round(predict_price))+" $"
        return render_template('base.html', color="green", msg=msg, weight= weight, price=price)

    return render_template('base.html')

if __name__ == '__main__':
    app.run()
