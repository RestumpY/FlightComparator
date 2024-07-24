from flask import Flask, request, render_template, jsonify
from datetime import datetime
from parse import parse
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrap', methods=['POST'])
def scrap():
    depart = request.form['ville_depart']
    destination = request.form['ville_arrive']
    dateDepart = request.form['date_depart']
    dateDepart = datetime.strptime(dateDepart, '%Y-%m-%d').strftime("%d/%m")
    dateArrive = request.form['date_arrive']
    dateArrive = datetime.strptime(dateArrive, '%Y-%m-%d').strftime("%d/%m")

    classe = request.form['classe']

    # Appel de la fonction de scrapping
    items = parse(depart, destination, classe, dateDepart, dateArrive)

    # Convertir les objets Item en dictionnaires
    items_list = [item.to_dict() for item in items]

    # Retourner les données JSON
    return jsonify(items_list)

if __name__ == '__main__':
    app.run(debug=True)
