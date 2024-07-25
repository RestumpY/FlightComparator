from flask import Flask, request, render_template, jsonify
from datetime import datetime
from parse import parse
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap():
    ville_depart = request.form['ville_depart']
    ville_arrive = request.form['ville_arrive']
    date_depart = request.form['date_depart']
    date_depart = datetime.strptime(date_depart, '%Y-%m-%d').strftime("%d/%m")
    date_arrive = request.form['date_arrive']
    date_arrive = datetime.strptime(date_arrive, '%Y-%m-%d').strftime("%d/%m")
    classe = request.form['classe']

    # Encodage de la classe
    class_encoded = 2 if classe == 'Business' else 1

    # Appel à la fonction de parsing
    items = parse(ville_depart, ville_arrive, classe, date_depart, date_arrive)

    # Convertir les éléments en une liste de dictionnaires
    items_list = [item.to_dict() for item in items]

    # Faire les prédictions pour chaque élément
    for item in items_list:
        duration = item['dureeConvert']

        input_data = {
            'class_encoded': class_encoded,
            'duration': duration,
        }

        # Faire la prédiction avec l'API R
        response = requests.get('http://127.0.0.1:8000/predict', params=input_data)
        predicted_price = response.json()['prediction']

        item['predicted_price'] = predicted_price

    return jsonify(items_list)


if __name__ == '__main__':
    app.run(debug=True)
