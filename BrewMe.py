from flask import Flask, render_template
from flask import request
from BrewMeFunct import search
import time
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def main():
    return render_template('main.html', results=None)

@app.route("/search", methods = ['POST'])
def do_search():
    addr = request.form['inputAddress']
    city = request.form['inputCity']
    state = request.form['inputState']
    radius = int(request.form['inputRadius'])

    return render_template('main.html', title='Results', results=sorted(search(addr, city, state, radius), key=lambda i: i['distance']), input_data=[addr, city, state, radius])

if __name__ == "__main__":
    app.run(debug=True)