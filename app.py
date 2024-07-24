from flask import Flask, request, render_template, jsonify
from datetime import datetime
from parse import parse

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

    # Call the scraping function
    items = parse(ville_depart, ville_arrive, classe, date_depart, date_arrive)

    # Convert items to a list of dictionaries
    items_list = [item.to_dict() for item in items]

    return jsonify(items_list)

if __name__ == '__main__':
    app.run(debug=True)
