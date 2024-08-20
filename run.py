from flask import Flask, jsonify, url_for, render_template
from scrapper import Komikcast
app = Flask(__name__)

@app.route('/')
def root():
    kcast = Komikcast()
    return render_template('index.html', hot=kcast.hot_update(), update=kcast.update())

app.run(debug=True)
